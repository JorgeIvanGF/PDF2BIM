from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_wall_analysis_endpoint_runs_end_to_end(vector_pdf_bytes: bytes) -> None:
    upload = client.post(
        "/api/documents",
        files={"file": ("fixture.pdf", vector_pdf_bytes, "application/pdf")},
    )
    document_id = upload.json()["document_id"]

    # El fixture contiene dos líneas a 20 unidades PDF. Las calibramos como 200 mm.
    response = client.post(
        f"/api/documents/{document_id}/analyze-walls",
        json={
            "page": 1,
            "calibration": {
                "point_a": {"x": 100, "y": 150},
                "point_b": {"x": 500, "y": 150},
                "real_distance_mm": 4000
            },
            "wall_types": [
                {"id": "wall-200", "name": "Muro 200", "nominal_thickness_mm": 200, "tolerance_mm": 15}
            ]
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["raw_segment_count"] == 7
    assert body["normalized_segment_count"] == 6
    assert any(w["wall_type_rule_id"] == "wall-200" for w in body["wall_candidates"])
