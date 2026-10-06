from __future__ import annotations

import fitz

from app.pdf.preflight import inspect_document
from app.pdf.reader import extract_page_geometry


def test_extracts_line_and_rectangle_segments(vector_pdf_bytes: bytes) -> None:
    doc = fitz.open(stream=vector_pdf_bytes, filetype="pdf")
    geometry = extract_page_geometry(doc[0])

    # PyMuPDF conserva la geometría cruda; el fixture incluye 4 lados, 2 líneas y un cierre inverso duplicado.
    assert len(geometry.segments) == 7
    assert geometry.width == 600
    assert geometry.height == 400
    assert all(segment.page_number == 1 for segment in geometry.segments)


def test_preflight_marks_vector_pdf_compatible(vector_pdf_bytes: bytes) -> None:
    result = inspect_document(vector_pdf_bytes, "vector.pdf")

    assert result.vector_compatible is True
    assert result.page_count == 1
    assert result.total_segments == 7
    assert result.total_drawing_paths >= 1


def test_preflight_rejects_raster_only_document(raster_only_pdf_bytes: bytes) -> None:
    result = inspect_document(raster_only_pdf_bytes, "scan.pdf")

    assert result.vector_compatible is False
    assert result.total_segments == 0
    assert result.total_images >= 1
    assert result.warnings
