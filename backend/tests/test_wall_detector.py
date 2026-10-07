from __future__ import annotations

import math
import random

from app.domain.analysis import NormalizedSegment2D, WallTypeRule
from app.domain.geometry import Point2D, StrokeStyle
from app.geometry.walls import (
    _detect_candidates_from_pairs,
    _spatial_candidate_pairs,
    detect_wall_candidates,
)


def nseg(segment_id: str, x1: float, y1: float, x2: float, y2: float) -> NormalizedSegment2D:
    length = math.hypot(x2 - x1, y2 - y1)
    angle = math.degrees(math.atan2(y2-y1, x2-x1)) % 180
    return NormalizedSegment2D(
        id=segment_id,
        page_number=1,
        start=Point2D(x=x1, y=y1),
        end=Point2D(x=x2, y=y2),
        length_pdf=length,
        angle_deg=angle,
        source_segment_ids=[segment_id],
        style=StrokeStyle(),
    )


def rules() -> list[WallTypeRule]:
    return [
        WallTypeRule(id="wall-100", name="Muro 100", nominal_thickness_mm=100, tolerance_mm=15),
        WallTypeRule(id="wall-200", name="Muro 200", nominal_thickness_mm=200, tolerance_mm=15),
    ]


def test_detects_horizontal_200mm_wall_and_computes_axis() -> None:
    # 1 PDF unit = 10 mm, por tanto separación de 20 = 200 mm.
    segments = [
        nseg("top", 10, 20, 110, 20),
        nseg("bottom", 10, 40, 110, 40),
    ]
    found = detect_wall_candidates(
        segments,
        mm_per_pdf_unit=10,
        rules=rules(),
        angular_tolerance_deg=1.5,
        min_overlap_mm=300,
        min_overlap_ratio=0.45,
    )

    assert len(found) == 1
    wall = found[0]
    assert wall.wall_type_rule_id == "wall-200"
    assert math.isclose(wall.measured_thickness_mm, 200)
    assert math.isclose(wall.axis_start_mm.y, 300)
    assert math.isclose(wall.axis_end_mm.y, 300)
    assert math.isclose(wall.length_mm, 1000)
    assert wall.confidence_score > 0.99


def test_rejects_parallel_lines_with_unknown_thickness() -> None:
    segments = [nseg("a", 0, 0, 100, 0), nseg("b", 0, 30, 100, 30)]
    found = detect_wall_candidates(
        segments,
        mm_per_pdf_unit=10,
        rules=rules(),
        angular_tolerance_deg=1.5,
        min_overlap_mm=300,
        min_overlap_ratio=0.45,
    )
    assert found == []


def test_rejects_non_overlapping_parallel_lines() -> None:
    segments = [nseg("a", 0, 0, 100, 0), nseg("b", 120, 20, 220, 20)]
    found = detect_wall_candidates(
        segments,
        mm_per_pdf_unit=10,
        rules=rules(),
        angular_tolerance_deg=1.5,
        min_overlap_mm=300,
        min_overlap_ratio=0.45,
    )
    assert found == []


def test_rejects_pair_whose_overlap_only_covers_a_small_fraction_of_longer_segment() -> None:
    # The shorter line is fully covered, but the common interval is only 20% of the longer line.
    segments = [
        nseg("long-wall-face", 0, 0, 500, 0),
        nseg("short-detail-line", 100, 10, 200, 10),
    ]
    found = detect_wall_candidates(
        segments,
        mm_per_pdf_unit=10,
        rules=rules(),
        angular_tolerance_deg=1.5,
        min_overlap_mm=300,
        min_overlap_ratio=0.45,
    )
    assert found == []


def test_keeps_wall_pair_with_sufficient_overlap_on_both_source_segments() -> None:
    segments = [
        nseg("long-wall-face", 0, 0, 200, 0),
        nseg("partial-wall-face", 25, 20, 175, 20),
    ]
    found = detect_wall_candidates(
        segments,
        mm_per_pdf_unit=10,
        rules=rules(),
        angular_tolerance_deg=1.5,
        min_overlap_mm=300,
        min_overlap_ratio=0.45,
    )
    assert len(found) == 1
    assert found[0].wall_type_rule_id == "wall-200"
    assert math.isclose(found[0].length_mm, 1500)


def test_spatial_index_matches_exhaustive_pair_search() -> None:
    rng = random.Random(1702)
    segments = [
        nseg("wall-a", 0, 0, 120, 0),
        nseg("wall-b", 0, 20, 120, 20),
        nseg("wrap-a", 0, 300, -120, 301.047),
        nseg("wrap-b", 0, 320, 120, 321.047),
    ]
    for index in range(96):
        angle = rng.choice((0.2, 1.4, 45.0, 89.8, 90.5, 178.8))
        length = rng.uniform(10, 240)
        x, y = rng.uniform(-300, 700), rng.uniform(-300, 700)
        radians = math.radians(angle)
        segments.append(
            nseg(
                f"random-{index}",
                x,
                y,
                x + math.cos(radians) * length,
                y + math.sin(radians) * length,
            )
        )

    arguments = {
        "mm_per_pdf_unit": 10,
        "rules": rules(),
        "angular_tolerance_deg": 1.5,
        "min_overlap_mm": 300,
        "min_overlap_ratio": 0.45,
    }
    exhaustive_pairs = (
        (first, second)
        for first in range(len(segments))
        for second in range(first + 1, len(segments))
    )
    indexed_pairs = list(
        _spatial_candidate_pairs(
            segments,
            mm_per_pdf_unit=arguments["mm_per_pdf_unit"],
            rules=arguments["rules"],
            angular_tolerance_deg=arguments["angular_tolerance_deg"],
        )
    )
    exhaustive_results = _detect_candidates_from_pairs(segments, exhaustive_pairs, **arguments)
    indexed_results = _detect_candidates_from_pairs(segments, iter(indexed_pairs), **arguments)

    assert [item.model_dump() for item in indexed_results] == [item.model_dump() for item in exhaustive_results]
    assert len(indexed_pairs) < len(segments) * (len(segments) - 1) // 2
