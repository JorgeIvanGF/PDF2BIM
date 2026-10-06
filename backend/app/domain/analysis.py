from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, model_validator

from app.domain.geometry import Point2D, StrokeStyle


class NormalizedSegment2D(BaseModel):
    id: str
    page_number: int
    start: Point2D
    end: Point2D
    length_pdf: float
    angle_deg: float
    source_segment_ids: list[str]
    style: StrokeStyle


class CalibrationInput(BaseModel):
    point_a: Point2D
    point_b: Point2D
    real_distance_mm: float = Field(gt=0)

    @model_validator(mode="after")
    def points_must_differ(self) -> "CalibrationInput":
        if self.point_a.x == self.point_b.x and self.point_a.y == self.point_b.y:
            raise ValueError("Los puntos de calibración deben ser distintos.")
        return self


class CalibrationResult(BaseModel):
    mm_per_pdf_unit: float = Field(gt=0)
    measured_pdf_distance: float = Field(gt=0)
    real_distance_mm: float = Field(gt=0)


class WallTypeRule(BaseModel):
    id: str
    name: str
    nominal_thickness_mm: float = Field(gt=0)
    tolerance_mm: float = Field(gt=0)


class WallCandidateStatus(str, Enum):
    DETECTED = "DETECTED"
    CONFIRMED = "CONFIRMED"
    MODIFIED = "MODIFIED"
    REJECTED = "REJECTED"


class WallCandidate(BaseModel):
    id: str
    axis_start_mm: Point2D
    axis_end_mm: Point2D
    measured_thickness_mm: float
    nominal_thickness_mm: float
    length_mm: float
    wall_type_rule_id: str
    wall_type_name: str
    confidence_score: float = Field(ge=0, le=1)
    source_segment_ids: tuple[str, str]
    status: WallCandidateStatus = WallCandidateStatus.DETECTED
    warnings: list[str] = []


class WallAnalysisRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    calibration: CalibrationInput
    wall_types: list[WallTypeRule] = Field(min_length=1)
    angular_tolerance_deg: float = Field(default=1.5, gt=0, le=10)
    min_overlap_mm: float = Field(default=300, gt=0)
    min_overlap_ratio: float = Field(default=0.45, gt=0, le=1)


class WallAnalysisResponse(BaseModel):
    page_number: int
    raw_segment_count: int
    normalized_segment_count: int
    calibration: CalibrationResult
    wall_candidates: list[WallCandidate]
    warnings: list[str] = []
