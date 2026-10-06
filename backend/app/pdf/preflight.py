from __future__ import annotations

import fitz

from app.domain.documents import DocumentPreflight, PagePreflight
from app.pdf.reader import extract_page_geometry


def inspect_document(pdf_bytes: bytes, filename: str) -> DocumentPreflight:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages: list[PagePreflight] = []

    total_paths = 0
    total_segments = 0
    total_images = 0
    total_text_blocks = 0
    total_unsupported = 0

    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        drawings = page.get_drawings()
        geometry = extract_page_geometry(page)
        images = page.get_images(full=True)
        text_blocks = page.get_text("blocks")

        total_paths += len(drawings)
        total_segments += len(geometry.segments)
        total_images += len(images)
        total_text_blocks += len(text_blocks)
        total_unsupported += geometry.unsupported_item_count

        pages.append(
            PagePreflight(
                page_number=page_index + 1,
                width=float(page.rect.width),
                height=float(page.rect.height),
                drawing_path_count=len(drawings),
                extracted_segment_count=len(geometry.segments),
                image_count=len(images),
                text_block_count=len(text_blocks),
                unsupported_vector_item_count=geometry.unsupported_item_count,
            )
        )

    warnings: list[str] = []
    vector_compatible = total_segments > 0

    if not vector_compatible:
        warnings.append(
            "No se encontraron segmentos vectoriales compatibles. El documento puede ser escaneado o usar geometría aún no soportada."
        )
    if total_unsupported:
        warnings.append(
            f"Se encontraron {total_unsupported} elementos vectoriales todavía no convertidos a segmentos rectos (por ejemplo, curvas)."
        )
    if doc.page_count > 1:
        warnings.append("El MVP inicial analiza una página a la vez.")

    return DocumentPreflight(
        filename=filename,
        page_count=doc.page_count,
        vector_compatible=vector_compatible,
        total_drawing_paths=total_paths,
        total_segments=total_segments,
        total_images=total_images,
        total_text_blocks=total_text_blocks,
        pages=pages,
        warnings=warnings,
    )
