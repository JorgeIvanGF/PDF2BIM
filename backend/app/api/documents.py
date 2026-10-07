from __future__ import annotations

import fitz
from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from app.domain.documents import DocumentCreated, DocumentMetadata
from app.domain.analysis import WallAnalysisRequest, WallAnalysisResponse
from app.domain.geometry import PageGeometry
from app.geometry.calibration import calculate_calibration
from app.geometry.normalize import normalize_page_geometry
from app.geometry.walls import detect_wall_candidates
from app.pdf.preflight import inspect_document
from app.pdf.reader import extract_page_geometry
from app.services.document_store import store

router = APIRouter(prefix="/documents", tags=["documents"])

MAX_FILE_BYTES = 25 * 1024 * 1024


@router.post("", response_model=DocumentCreated, status_code=status.HTTP_201_CREATED)
async def create_document(file: UploadFile = File(...)) -> DocumentCreated:
    filename = file.filename or "document.pdf"
    content_type = file.content_type or "application/octet-stream"

    if content_type != "application/pdf" and not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Solo se aceptan archivos PDF.")

    data = await file.read(MAX_FILE_BYTES + 1)
    if not data:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")
    if len(data) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="El PDF supera el límite de 25 MB del prototipo.")

    try:
        preflight = inspect_document(data, filename)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="El archivo no pudo interpretarse como PDF válido.") from exc

    stored = store.save(
        filename=filename,
        content_type=content_type,
        data=data,
        preflight=preflight,
    )
    return DocumentCreated(document_id=stored.metadata.document_id, preflight=preflight)


@router.get("/{document_id}", response_model=DocumentMetadata)
def get_document(document_id: str) -> DocumentMetadata:
    stored = store.get(document_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")
    return stored.metadata


@router.get("/{document_id}/geometry", response_model=PageGeometry)
def get_geometry(
    document_id: str,
    page: int = Query(default=1, ge=1),
) -> PageGeometry:
    stored = store.get(document_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")

    try:
        doc = fitz.open(stored.path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="No fue posible abrir el PDF almacenado.") from exc

    if page > doc.page_count:
        raise HTTPException(status_code=404, detail="La página solicitada no existe.")

    return extract_page_geometry(doc.load_page(page - 1))


@router.post("/{document_id}/analyze-walls", response_model=WallAnalysisResponse)
def analyze_walls(document_id: str, request: WallAnalysisRequest) -> WallAnalysisResponse:
    stored = store.get(document_id)
    if stored is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")

    doc = fitz.open(stored.path)
    if request.page > doc.page_count:
        raise HTTPException(status_code=404, detail="La página solicitada no existe.")

    raw = extract_page_geometry(doc.load_page(request.page - 1))
    normalized = normalize_page_geometry(raw)
    calibration = calculate_calibration(request.calibration)
    candidates = detect_wall_candidates(
        normalized,
        mm_per_pdf_unit=calibration.mm_per_pdf_unit,
        rules=request.wall_types,
        angular_tolerance_deg=request.angular_tolerance_deg,
        min_overlap_mm=request.min_overlap_mm,
        min_overlap_ratio=request.min_overlap_ratio,
    )

    return WallAnalysisResponse(
        page_number=request.page,
        raw_segment_count=len(raw.segments),
        normalized_segment_count=len(normalized),
        calibration=calibration,
        wall_candidates=candidates,
    )
