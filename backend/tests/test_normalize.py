from __future__ import annotations

from app.domain.geometry import PageGeometry, Point2D, Segment2D, StrokeStyle
from app.geometry.normalize import normalize_page_geometry


def segment(segment_id: str, x1: float, y1: float, x2: float, y2: float) -> Segment2D:
    return Segment2D(
        id=segment_id,
        page_number=1,
        start=Point2D(x=x1, y=y1),
        end=Point2D(x=x2, y=y2),
        source_path_index=0,
        source_item_index=0,
        source_kind="l",
        style=StrokeStyle(),
    )


def test_normalization_collapses_exact_reversed_duplicate() -> None:
    page = PageGeometry(
        page_number=1,
        width=100,
        height=100,
        segments=[
            segment("a", 10, 20, 90, 20),
            segment("b", 90, 20, 10, 20),
        ],
    )
    result = normalize_page_geometry(page)

    assert len(result) == 1
    assert result[0].source_segment_ids == ["a", "b"]
    assert result[0].length_pdf == 80
    assert result[0].angle_deg == 0


def test_normalization_removes_degenerate_segment() -> None:
    page = PageGeometry(
        page_number=1,
        width=100,
        height=100,
        segments=[segment("zero", 10, 10, 10, 10)],
    )
    assert normalize_page_geometry(page) == []
