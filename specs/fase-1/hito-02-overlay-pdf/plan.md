# F01-H02 — Plan

El archivo PDF no necesita volver al backend para visualizarse: el frontend conserva el `File` seleccionado y PDF.js lo procesa localmente.

```text
File PDF ──> PDF.js ──> Canvas
                 +
PageGeometry ──> SVG overlay
```

El SVG usa `viewBox="0 0 width height"` con las dimensiones devueltas por PyMuPDF. El contenedor fuerza la misma relación de aspecto que la geometría del backend.
