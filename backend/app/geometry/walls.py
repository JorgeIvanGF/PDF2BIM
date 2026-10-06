from __future__ import annotations

from dataclasses import dataclass
import math

from app.domain.analysis import NormalizedSegment2D, WallCandidate, WallTypeRule
from app.domain.geometry import Point2D


@dataclass(frozen=True)
class _Vec:
    x: float
    y: float

    def dot(self, other: "_Vec") -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other: "_Vec") -> float:
        return self.x * other.y - self.y * other.x

    def scale(self, value: float) -> "_Vec":
        return _Vec(self.x * value, self.y * value)

    def plus(self, other: "_Vec") -> "_Vec":
        return _Vec(self.x + other.x, self.y + other.y)


def _vec(a: Point2D, b: Point2D) -> _Vec:
    return _Vec(b.x - a.x, b.y - a.y)


def _length(v: _Vec) -> float:
    return math.hypot(v.x, v.y)


def _unit(v: _Vec) -> _Vec:
    size = _length(v)
    return _Vec(v.x / size, v.y / size)


def _angle_delta(a: float, b: float) -> float:
    delta = abs(a - b) % 180.0
    return min(delta, 180.0 - delta)


def _best_rule(distance_mm: float, rules: list[WallTypeRule]) -> WallTypeRule | None:
    compatible = [r for r in rules if abs(distance_mm - r.nominal_thickness_mm) <= r.tolerance_mm]
    if not compatible:
        return None
    return min(compatible, key=lambda r: abs(distance_mm - r.nominal_thickness_mm))


def _parallel_metrics(
    a: NormalizedSegment2D,
    b: NormalizedSegment2D,
    mm_per_pdf_unit: float,
) -> tuple[float, float, float, Point2D, Point2D] | None:
    """Return thickness_mm, overlap_mm, overlap_ratio, axis_start_mm, axis_end_mm.

    The axis is computed on the overlapping interval. For the MVP, small angular deviations are
    allowed by the caller; projection uses segment A as the reference direction.
    """
    a0 = _Vec(a.start.x, a.start.y)
    a1 = _Vec(a.end.x, a.end.y)
    b0 = _Vec(b.start.x, b.start.y)
    b1 = _Vec(b.end.x, b.end.y)

    direction = _unit(_Vec(a1.x - a0.x, a1.y - a0.y))
    normal = _Vec(-direction.y, direction.x)

    # Project both segments onto A's longitudinal axis.
    def longitudinal(point: _Vec) -> float:
        return _Vec(point.x - a0.x, point.y - a0.y).dot(direction)

    a_t0, a_t1 = sorted((longitudinal(a0), longitudinal(a1)))
    b_t0, b_t1 = sorted((longitudinal(b0), longitudinal(b1)))
    overlap_start = max(a_t0, b_t0)
    overlap_end = min(a_t1, b_t1)
    overlap_pdf = overlap_end - overlap_start
    if overlap_pdf <= 0:
        return None

    # Signed distances of B endpoints to A's infinite line; average is stable for near-parallel lines.
    d0 = _Vec(b0.x - a0.x, b0.y - a0.y).dot(normal)
    d1 = _Vec(b1.x - a0.x, b1.y - a0.y).dot(normal)
    signed_offset = (d0 + d1) / 2.0
    thickness_pdf = abs(signed_offset)

    min_len_pdf = min(a.length_pdf, b.length_pdf)
    overlap_ratio = overlap_pdf / min_len_pdf if min_len_pdf > 0 else 0

    # Axis = middle of A reference line and the estimated parallel line through B.
    midpoint_offset = normal.scale(signed_offset / 2.0)
    axis_start_pdf = a0.plus(direction.scale(overlap_start)).plus(midpoint_offset)
    axis_end_pdf = a0.plus(direction.scale(overlap_end)).plus(midpoint_offset)

    factor = mm_per_pdf_unit
    return (
        thickness_pdf * factor,
        overlap_pdf * factor,
        overlap_ratio,
        Point2D(x=axis_start_pdf.x * factor, y=axis_start_pdf.y * factor),
        Point2D(x=axis_end_pdf.x * factor, y=axis_end_pdf.y * factor),
    )


def detect_wall_candidates(
    segments: list[NormalizedSegment2D],
    *,
    mm_per_pdf_unit: float,
    rules: list[WallTypeRule],
    angular_tolerance_deg: float,
    min_overlap_mm: float,
    min_overlap_ratio: float,
) -> list[WallCandidate]:
    candidates: list[WallCandidate] = []

    # MVP correctness-first implementation. Spatial indexing is scheduled after real-plan profiling.
    for i, first in enumerate(segments):
        for second in segments[i + 1 :]:
            angle_error = _angle_delta(first.angle_deg, second.angle_deg)
            if angle_error > angular_tolerance_deg:
                continue

            metrics = _parallel_metrics(first, second, mm_per_pdf_unit)
            if metrics is None:
                continue
            thickness_mm, overlap_mm, overlap_ratio, axis_start, axis_end = metrics

            if overlap_mm < min_overlap_mm or overlap_ratio < min_overlap_ratio:
                continue

            rule = _best_rule(thickness_mm, rules)
            if rule is None:
                continue

            thickness_error = abs(thickness_mm - rule.nominal_thickness_mm)
            angle_score = max(0.0, 1.0 - angle_error / angular_tolerance_deg)
            thickness_score = max(0.0, 1.0 - thickness_error / rule.tolerance_mm)
            overlap_score = min(1.0, overlap_ratio)
            confidence = 0.35 * angle_score + 0.40 * thickness_score + 0.25 * overlap_score

            length_mm = math.hypot(axis_end.x - axis_start.x, axis_end.y - axis_start.y)
            candidates.append(
                WallCandidate(
                    id=f"w-{len(candidates) + 1}",
                    axis_start_mm=axis_start,
                    axis_end_mm=axis_end,
                    measured_thickness_mm=thickness_mm,
                    nominal_thickness_mm=rule.nominal_thickness_mm,
                    length_mm=length_mm,
                    wall_type_rule_id=rule.id,
                    wall_type_name=rule.name,
                    confidence_score=round(confidence, 6),
                    source_segment_ids=(first.id, second.id),
                )
            )

    return sorted(candidates, key=lambda item: item.confidence_score, reverse=True)
