from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import fitz

from app.domain.geometry import PageGeometry, Point2D, Segment2D, StrokeStyle


@dataclass(frozen=True)
class ExtractionStats:
    unsupported_item_count: int


def _rgb_tuple(value: object) -> tuple[float, float, float] | None:
    if not isinstance(value, (list, tuple)) or len(value) < 3:
        return None
    return (float(value[0]), float(value[1]), float(value[2]))


def _point(value: object) -> Point2D:
    if isinstance(value, fitz.Point):
        return Point2D(x=float(value.x), y=float(value.y))
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return Point2D(x=float(value[0]), y=float(value[1]))
    raise TypeError(f"Unsupported point representation: {type(value)!r}")


def _rectangle_segments(rect: fitz.Rect | tuple[float, float, float, float]) -> Iterable[tuple[Point2D, Point2D]]:
    r = fitz.Rect(rect)
    p1 = Point2D(x=float(r.x0), y=float(r.y0))
    p2 = Point2D(x=float(r.x1), y=float(r.y0))
    p3 = Point2D(x=float(r.x1), y=float(r.y1))
    p4 = Point2D(x=float(r.x0), y=float(r.y1))
    return ((p1, p2), (p2, p3), (p3, p4), (p4, p1))


def extract_page_geometry(page: fitz.Page) -> PageGeometry:
    drawings = page.get_drawings()
    segments: list[Segment2D] = []
    unsupported = 0

    for path_index, path in enumerate(drawings):
        style = StrokeStyle(
            width=float(path["width"]) if path.get("width") is not None else None,
            color_rgb=_rgb_tuple(path.get("color")),
            dashes=str(path.get("dashes")) if path.get("dashes") else None,
            opacity=float(path["stroke_opacity"]) if path.get("stroke_opacity") is not None else None,
        )

        for item_index, item in enumerate(path.get("items", [])):
            kind = item[0]
            line_pairs: Iterable[tuple[Point2D, Point2D]]

            if kind == "l" and len(item) >= 3:
                line_pairs = ((_point(item[1]), _point(item[2])),)
            elif kind == "re" and len(item) >= 2:
                line_pairs = _rectangle_segments(item[1])
            else:
                unsupported += 1
                continue

            for local_index, (start, end) in enumerate(line_pairs):
                segments.append(
                    Segment2D(
                        id=f"p{page.number + 1}-path{path_index}-item{item_index}-s{local_index}",
                        page_number=page.number + 1,
                        start=start,
                        end=end,
                        source_path_index=path_index,
                        source_item_index=item_index,
                        source_kind=kind,
                        style=style,
                    )
                )

    rect = page.rect
    return PageGeometry(
        page_number=page.number + 1,
        width=float(rect.width),
        height=float(rect.height),
        segments=segments,
        unsupported_item_count=unsupported,
    )
