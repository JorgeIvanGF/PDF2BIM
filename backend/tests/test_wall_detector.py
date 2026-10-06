from __future__ import annotations

import math

from app.domain.analysis import NormalizedSegment2D, WallTypeRule
from app.domain.geometry import Point2D, StrokeStyle
from app.geometry.walls import detect_wall_candidates


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
