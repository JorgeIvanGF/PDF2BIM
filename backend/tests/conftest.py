from __future__ import annotations

from pathlib import Path

import fitz
import pytest


@pytest.fixture()
def vector_pdf_bytes() -> bytes:
    doc = fitz.open()
    page = doc.new_page(width=600, height=400)

    shape = page.new_shape()
    shape.draw_rect(fitz.Rect(50, 50, 550, 350))
    shape.draw_line(fitz.Point(100, 150), fitz.Point(500, 150))
    shape.draw_line(fitz.Point(100, 170), fitz.Point(500, 170))
    shape.finish(color=(0, 0, 0), width=1)
    shape.commit()

    page.insert_text((60, 30), "Fixture vectorial PDF2BIM")
    return doc.tobytes()


@pytest.fixture()
def raster_only_pdf_bytes() -> bytes:
    pix_doc = fitz.open()
    pix_page = pix_doc.new_page(width=200, height=100)
    pix_page.draw_rect(fitz.Rect(0, 0, 200, 100), color=(0, 0, 0), fill=(1, 1, 1))
    pix = pix_page.get_pixmap()

    doc = fitz.open()
    page = doc.new_page(width=600, height=400)
    page.insert_image(page.rect, pixmap=pix)
    return doc.tobytes()
