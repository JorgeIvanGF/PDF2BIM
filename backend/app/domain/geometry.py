from __future__ import annotations

from pydantic import BaseModel, Field


class Point2D(BaseModel):
    x: float
    y: float


class StrokeStyle(BaseModel):
    width: float | None = None
    color_rgb: tuple[float, float, float] | None = None
    dashes: str | None = None
    opacity: float | None = None


class Segment2D(BaseModel):
    id: str
    page_number: int = Field(ge=1)
    start: Point2D
    end: Point2D
    source_path_index: int = Field(ge=0)
    source_item_index: int = Field(ge=0)
    source_kind: str
    style: StrokeStyle


class PageGeometry(BaseModel):
    page_number: int
    width: float
    height: float
    segments: list[Segment2D]
    unsupported_item_count: int = 0
