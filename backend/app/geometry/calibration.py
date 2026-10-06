from __future__ import annotations

import math

from app.domain.analysis import CalibrationInput, CalibrationResult


def calculate_calibration(value: CalibrationInput) -> CalibrationResult:
    pdf_distance = math.hypot(
        value.point_b.x - value.point_a.x,
        value.point_b.y - value.point_a.y,
    )
    if pdf_distance <= 0:
        raise ValueError("La distancia PDF debe ser mayor que cero.")

    return CalibrationResult(
        mm_per_pdf_unit=value.real_distance_mm / pdf_distance,
        measured_pdf_distance=pdf_distance,
        real_distance_mm=value.real_distance_mm,
    )
