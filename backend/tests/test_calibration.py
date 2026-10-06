from __future__ import annotations

import math

from app.domain.analysis import CalibrationInput
from app.domain.geometry import Point2D
from app.geometry.calibration import calculate_calibration


def test_calibration_calculates_mm_per_pdf_unit() -> None:
    result = calculate_calibration(
        CalibrationInput(
            point_a=Point2D(x=0, y=0),
            point_b=Point2D(x=300, y=400),
            real_distance_mm=5000,
        )
    )
    assert math.isclose(result.measured_pdf_distance, 500)
    assert math.isclose(result.mm_per_pdf_unit, 10)
