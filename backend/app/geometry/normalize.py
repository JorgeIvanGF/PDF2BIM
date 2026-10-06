from __future__ import annotations

import math

from app.domain.analysis import NormalizedSegment2D
from app.domain.geometry import PageGeometry, Point2D, Segment2D

EPSILON = 1e-6


def _distance(a: Point2D, b: Point2D) -> float:
    return math.hypot(b.x - a.x, b.y - a.y)


def _canonical_points(a: Point2D, b: Point2D) -> tuple[Point2D, Point2D]:
    if (a.x, a.y) <= (b.x, b.y):
        return a, b
    return b, a


def _angle_deg(a: Point2D, b: Point2D) -> float:
    angle = math.degrees(math.atan2(b.y - a.y, b.x - a.x)) % 180.0
    if math.isclose(angle, 180.0, abs_tol=EPSILON):
        return 0.0
    return angle


def _key(a: Point2D, b: Point2D) -> tuple[int, int, int, int]:
    # Hito de normalización pre-calibración: solo colapsa duplicados prácticamente exactos.
    # La cuantización evita diferencias flotantes de serialización sin introducir tolerancias arquitectónicas.
    scale = 1_000_000
    return (
        round(a.x * scale),
        round(a.y * scale),
        round(b.x * scale),
        round(b.y * scale),
    )


def normalize_page_geometry(page: PageGeometry) -> list[NormalizedSegment2D]:
    by_key: dict[tuple[int, int, int, int], NormalizedSegment2D] = {}

    for raw in page.segments:
        start, end = _canonical_points(raw.start, raw.end)
        length = _distance(start, end)
        if length <= EPSILON:
            continue

        key = _key(start, end)
        existing = by_key.get(key)
        if existing:
            existing.source_segment_ids.append(raw.id)
            continue

        by_key[key] = NormalizedSegment2D(
            id=f"n-{len(by_key) + 1}",
            page_number=raw.page_number,
            start=start,
            end=end,
            length_pdf=length,
            angle_deg=_angle_deg(start, end),
            source_segment_ids=[raw.id],
            style=raw.style,
        )

    return list(by_key.values())
