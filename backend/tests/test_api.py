from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_upload_and_geometry_roundtrip(vector_pdf_bytes: bytes) -> None:
    upload = client.post(
        "/api/documents",
        files={"file": ("fixture.pdf", vector_pdf_bytes, "application/pdf")},
    )
    assert upload.status_code == 201
    payload = upload.json()
    assert payload["preflight"]["vector_compatible"] is True

    geometry = client.get(f"/api/documents/{payload['document_id']}/geometry?page=1")
    assert geometry.status_code == 200
    body = geometry.json()
    assert len(body["segments"]) == 7
    assert body["width"] == 600


def test_rejects_non_pdf() -> None:
    response = client.post(
        "/api/documents",
        files={"file": ("file.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415
