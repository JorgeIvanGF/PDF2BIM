# Changelog

## 0.1.2 — 2026-10-06
- Se cierra F01-H02 tras completar los criterios documentados, incluido el build frontend y la validación visual con `samples/PLANO PDF LEO.pdf`.
- El backend extrajo 11148 segmentos y PDF.js renderizó correctamente la lámina de una página.
- El usuario confirmó que el overlay SVG quedó alineado visualmente en la primera planta, que coinciden muros exteriores e interiores y líneas relevantes, y que la selección de puntos coincide con el clic y alcanza `2/2`.
- Esta validación no incluye el cierre de F01-H01 ni verifica la normalización, la calibración con cotas ni el detector de muros.

## 0.1.1 — 2026-10-05
- Hotfix del primer build Docker del frontend.
- Se añade `@types/three` 0.184.0 para resolver TS7016 en `Wall3DViewer.tsx`.
- `tsconfig.node.json` activa `noEmit: true`, requerido por `allowImportingTsExtensions` con TypeScript, resolviendo TS5096.
- Se incorpora `samples/plano-prueba-vectorial-01.pdf` como fixture controlada de 6 muros.
- La configuración `tsconfig.node.json` fue validada con TypeScript (`tsc --showConfig`).
- Build local verificado con `npm run build`: TypeScript y Vite completan correctamente.
- Se añade `frontend/package-lock.json` para reproducir el árbol de dependencias comprobado.
- La primera prueba de Docker Compose quedó bloqueada por DNS de Docker Hub; en una nueva sesión Docker Desktop respondió y el stack completo construyó e inició.
- La API procesó el fixture controlado con 6 candidatos: 4 de 200 mm y 2 de 100 mm.
- Validación de PC y proxy: frontend 200, health correcto y carga/consulta de geometría same-origin completadas.
- Nginx sirve `.mjs` como `application/javascript`, corrigiendo el error de importación del worker PDF.js observado en Chrome.
- El usuario reportó que frontend y health endpoint respondieron desde un teléfono en la Wi-Fi; F00-H02 queda cerrado al cumplir sus cinco criterios.

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
