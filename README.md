# PDF2BIM

> **Hotfix 0.1.1:** corrige el primer build Docker del frontend añadiendo `@types/three` y configurando `noEmit` en `tsconfig.node.json`.


Prototipo SDD para interpretar geometría vectorial de planos PDF y convertirla progresivamente en un modelo BIM verificable.

## Estado actual

- F00-H00 Fundamentos y arquitectura: **CERRADO**
- F00-H01 Extracción vectorial PDF: **EN VALIDACIÓN**
- F00-H02 Entorno de ejecución/prueba móvil: **EN VALIDACIÓN**
- F01-H00 Normalización geométrica: **EN VALIDACIÓN**
- F01-H01 Calibración: **EN VALIDACIÓN**
- F01-H02 Overlay PDF + geometría: **EN IMPLEMENTACIÓN / pendiente build**
- F02-H00 Detector inicial de muros: **EN VALIDACIÓN**
- F03-H00 Visor 3D That Open: **EN IMPLEMENTACIÓN / pendiente build**

El núcleo ya recibe un PDF vectorial, extrae y normaliza segmentos, permite calibrar el plano, detecta candidatos de muro rectos por paralelismo/espesor/solapamiento y calcula sus ejes. La UI superpone esa geometría sobre el PDF original, exporta JSON y contiene un visor 3D preliminar.

## Arquitectura actual

```text
PDF vectorial
    ↓
PyMuPDF
    ↓
Segment2D raw
    ↓
normalización
    ↓
calibración mm/u PDF
    ↓
detector determinista
    ↓
WallCandidate
    ├──→ overlay PDF.js + SVG
    ├──→ JSON
    └──→ That Open / Three.js (3D preliminar)
```

Revit, IFC, MCP e IA están deliberadamente fuera del núcleo actual.

## Prueba recomendada desde PC + móvil

Con Docker y un entorno con acceso a npm/PyPI:

```bash
docker compose up --build
```

Después:
- PC: abrir `http://localhost:8080`.
- Android en la misma Wi‑Fi: abrir `http://<IP-LAN-DEL-PC>:8080`.

Nginx sirve el frontend y reenvía `/api` al backend, por lo que el teléfono solo necesita acceder al puerto `8080` del PC.

## Backend local sin Docker

Requisitos recomendados: Python 3.12+.

```bash
cd backend
python -m venv .venv
# activar entorno
pip install -e .[dev]
uvicorn app.main:app --reload
```

API:
- `GET /api/health`
- `POST /api/documents`
- `GET /api/documents/{document_id}`
- `GET /api/documents/{document_id}/geometry?page=1`
- `POST /api/documents/{document_id}/analyze-walls`

## Frontend local sin Docker

```bash
cd frontend
npm install
npm run dev
```

Por defecto espera el backend en `http://localhost:8000/api`. Puede cambiarse con `VITE_API_BASE`.

## Pruebas backend

```bash
cd backend
pytest
```

## Restricción actual

El MVP inicial solo considera PDFs con geometría vectorial útil. Los PDFs puramente escaneados se diagnostican como no compatibles y no se procesan mediante OCR.
