# Changelog

## 0.1.1 — 2026-10-05
- Hotfix del primer build Docker del frontend.
- Se añade `@types/three` 0.184.0 para resolver TS7016 en `Wall3DViewer.tsx`.
- `tsconfig.node.json` activa `noEmit: true`, requerido por `allowImportingTsExtensions` con TypeScript, resolviendo TS5096.
- Se incorpora `samples/plano-prueba-vectorial-01.pdf` como fixture controlada de 6 muros.
- La configuración `tsconfig.node.json` fue validada con TypeScript (`tsc --showConfig`).
- Build local verificado con `npm run build`: TypeScript y Vite completan correctamente.
- Se añade `frontend/package-lock.json` para reproducir el árbol de dependencias comprobado.
- El build de Docker Compose quedó parcialmente bloqueado: backend construido, pero el daemon no resolvió Docker Hub para descargar las imágenes base del frontend.
- La API procesó el fixture controlado con 6 candidatos: 4 de 200 mm y 2 de 100 mm.

## 0.1.0 — 2026-10-05
- Formalización SDD del proyecto.
- F00-H00 cerrado.
- Backend FastAPI para carga temporal de PDF.
- Preflight vectorial/raster.
- Extracción de líneas y rectángulos con PyMuPDF.
- Contrato `Segment2D` y `PageGeometry`.
- Frontend React mobile-first para carga, diagnóstico y visualización SVG.
- Fixtures vectorial/raster.
- Suite inicial de pruebas backend.

### Incremento provisional
- Normalización con deduplicación exacta/invertida.
- Calibración PDF → milímetros.
- Detector determinista de pares paralelos por espesor y solapamiento.
- Generación de eje de `WallCandidate`.
- Endpoint end-to-end de análisis de muros.
- UI móvil para seleccionar dos puntos de calibración y visualizar ejes propuestos.

- Integración preliminar de That Open Engine para extrusión 3D de candidatos de muro.
- Navegación 2D/3D preparada en UI.

- Overlay PDF.js + SVG geométrico implementado para validación visual.
- Selección táctil de calibración sobre el PDF original.
- Exportación del análisis de muros a JSON desde frontend.

### Entorno de ejecución
- Dockerfile para FastAPI.
- Dockerfile multi-stage para frontend Vite + Nginx.
- Reverse proxy `/api` y fallback SPA.
- Docker Compose para prueba desde PC/Android mediante puerto `8080`.
- `vite-env.d.ts` añadido para tipos de variables Vite/imports de assets.
