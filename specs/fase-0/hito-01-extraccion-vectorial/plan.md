# F00-H01 — Plan

## Backend
- `POST /api/documents`: preflight y almacenamiento temporal.
- `GET /api/documents/{id}/geometry`: extracción por página.
- `PageGeometry` y `Segment2D` como contratos públicos.

## Extracción
PyMuPDF `Page.get_drawings()` es la única fuente geométrica en este hito.

Primitivas soportadas:
- `l`: línea.
- `re`: rectángulo convertido a cuatro líneas.

Toda otra primitiva se registra como unsupported para evitar reinterpretación silenciosa.

## Frontend
UI mobile-first que:
- selecciona PDF;
- muestra compatibilidad y métricas;
- consulta geometría;
- dibuja segmentos con SVG usando el mismo sistema de coordenadas PDF.

## Verificación
- pytest unitario + API integration.
- fixture sintético generado programáticamente.
- fixture raster negativo.
- posterior prueba con PDF real.

## Hallazgo de implementación
El fixture demuestra que PyMuPDF puede devolver un segmento de cierre inverso duplicado dentro de un mismo path. F00-H01 lo preserva deliberadamente como geometría cruda; su eliminación corresponde a F01-H00.
