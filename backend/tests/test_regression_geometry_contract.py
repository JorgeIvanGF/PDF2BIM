from __future__ import annotations

import math
import fitz

from app.pdf.reader import extract_page_geometry


def test_segment_coordinates_are_preserved_in_pdf_space(vector_pdf_bytes: bytes) -> None:
    doc = fitz.open(stream=vector_pdf_bytes, filetype="pdf")
    geometry = extract_page_geometry(doc[0])

    horizontal = [
        s for s in geometry.segments
        if math.isclose(s.start.y, 150.0, abs_tol=0.01)
        and math.isclose(s.end.y, 150.0, abs_tol=0.01)
    ]
    assert len(horizontal) == 1
    assert math.isclose(horizontal[0].start.x, 100.0, abs_tol=0.01)
    assert math.isclose(horizontal[0].end.x, 500.0, abs_tol=0.01)
