# Changelog

## 0.1.7: 2026-10-07
- T-012: análisis geométrico adicional de G6 y G9 en `samples/PLANO PDF LEO.pdf`. G6 produce 4 registros redundantes sobre un eje (líneas fuente representativas de 500.2/350.1 mm, separación 100.0 mm, solapamiento 350.1 mm, ratio 0.700); G9 produce 2 (líneas de 469.7 mm, separación 105.6 mm, solapamiento completo, ratio 1.000).
- No se implementa otro filtro: las señales analizadas de paralelismo, solapamiento, espesor, densidad local, cruces, estilos y redundancia no separan de forma segura ambos falsos positivos de muros cortos válidos.
- Se añaden 8 controles sintéticos positivos: muros de 350/470 mm y 100/200 mm de espesor, aislados y en encuentro. Todos se detectan. La suite backend pasa 19/19.
- Revalidación del PDF sin cambio de algoritmo: 726 candidatos totales, 6 registros en la primera planta, G6 y G9 presentes, 1830795 pares broadphase, salida equivalente a los 726 pares esperados tras el filtro, 197 grupos de eje redundantes con 661 registros y 9.453 s de detección directa. La API respondió upload 201 y análisis 200 en 13.282 s, con 0 advertencias.
- T-012 permanece parcial y F02-H00 EN VALIDACIÓN; no hay muro real confirmado y los controles sintéticos no sustituyen una referencia positiva real.

## 0.1.6: 2026-10-07
- T-011 perfilado con `samples/PLANO PDF LEO.pdf`: 11148 segmentos raw, 10360 normalizados, 968 candidatos y 204.796 s de detección exhaustiva.
- T-013 añade buckets angulares y una grilla espacial conservadora. En la misma muestra reduce los pares broadphase de 53659620 posibles a 1830795; la detección directa tarda 12.275 s. Una comparación exhaustiva diferencial confirmó los mismos 726 pares tras aplicar el filtro de solapamiento.
- T-012 cambia el ratio relativo para medir el solapamiento sobre la línea fuente más larga. La salida baja de 968 a 726 candidatos y en la primera planta de 34 a 6 registros. Desaparecen G1, G2, G4, G5, G7 y G8; G6 y G9 continúan como falsos positivos confirmados. G3 queda filtrado por geometría, sin clasificación semántica.
- La API se verificó con el PDF real: upload 201, análisis 200, 726 candidatos y ninguna advertencia obsoleta.
- Suite backend: 17/17 pruebas pasan; `compileall` también pasa. Persiste la advertencia deprecada de `starlette.testclient` respecto de httpx.
- La muestra no confirma ningún muro real, no mide precisión global y muestra tramos largos sin candidatos. T-012 sigue pendiente y F02-H00 permanece EN VALIDACIÓN.
- Se elimina del endpoint la advertencia obsoleta que anunciaba comparación exhaustiva e indexación futura.

## 0.1.5 — 2026-10-07
- Se cierra F00-H01 tras validar `samples/PLANO PDF LEO.pdf` mediante el flujo real de la aplicación.
- El preflight reconoció el documento como compatible: 1 página, 5176 paths, 11148 segmentos, 2 imágenes, 100 bloques de texto y 124 elementos vectoriales no convertidos.
- El upload respondió `201 Created` y la consulta de geometría por página respondió `200 OK`; el build frontend pasó.
- La evidencia cubre extracción de geometría recta y rectángulos. No valida curvas, identificación semántica de vistas ni detección de muros. No fue necesario repetir la prueba móvil de F00-H02.

## 0.1.4 — 2026-10-07
- Se cierra F01-H00 tras validar el normalizador existente sobre `samples/PLANO PDF LEO.pdf`.
- De 11148 segmentos extraídos, 10360 quedaron normalizados; se eliminaron 103 degenerados y se colapsaron 685 duplicados en 606 grupos, preservando 11045 IDs fuente.
- No se encontraron inconsistencias de canonicalización, longitud o ángulo; `backend/tests/test_normalize.py` pasó sus 2 pruebas.
- La validación cubre la geometría segmentada de la lámina completa. No valida curvas ni detección de muros y no modifica F02-H00.

## 0.1.3 — 2026-10-06
- Se cierra F01-H01 tras validar manualmente la calibración con `samples/PLANO PDF LEO.pdf`.
- El usuario confirmó la selección de los extremos de la cota `13,35` en la primera planta y la distancia real de 13350 mm; la interfaz llegó a `2/2`.
- Para los puntos `(274.9101868, 1539.3955078)` y `(1031.5212402, 1539.3955078)`, la distancia es 756.6110535 unidades PDF y el factor calculado es 17.6444686 mm/unidad PDF.
- La unidad de la cota no está declarada en el PDF; su interpretación como metros fue confirmada por el usuario para esta validación. Esta evidencia no modifica ni cierra F02-H00.

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
