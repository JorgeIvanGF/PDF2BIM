from __future__ import annotations

from pydantic import BaseModel, Field


class PagePreflight(BaseModel):
    page_number: int = Field(ge=1)
    width: float
    height: float
    drawing_path_count: int
    extracted_segment_count: int
    image_count: int
    text_block_count: int
    unsupported_vector_item_count: int


class DocumentPreflight(BaseModel):
    filename: str
    page_count: int
    vector_compatible: bool
    total_drawing_paths: int
    total_segments: int
    total_images: int
    total_text_blocks: int
    pages: list[PagePreflight]
    warnings: list[str]


class DocumentCreated(BaseModel):
    document_id: str
    preflight: DocumentPreflight


class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    content_type: str
    size_bytes: int
    preflight: DocumentPreflight
