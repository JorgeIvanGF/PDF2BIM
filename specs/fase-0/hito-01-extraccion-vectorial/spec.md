# F00-H01 — Extracción vectorial PDF

**Estado:** EN VALIDACIÓN

## Objetivo
Demostrar que PDF2BIM puede recibir un PDF vectorial y reconstruir segmentos rectos manteniendo las coordenadas originales de la página.

## Comportamiento
1. Usuario carga PDF.
2. Backend valida tipo/tamaño.
3. PyMuPDF inspecciona páginas y drawings.
4. Los comandos `l` se convierten en segmentos.
5. Los rectángulos `re` se descomponen en cuatro segmentos.
6. Curvas y otras primitivas se cuentan como no soportadas, sin falsificar segmentos.
7. API devuelve preflight y geometría por página.

## Alcance
- PDF válido hasta 25 MB.
- Diagnóstico vectorial/raster.
- Segmentos rectos.
- Rectángulos.
- Estilo de trazo básico.
- Una página visible por consulta.
- UI móvil de carga/diagnóstico/visualización geométrica.

## Exclusiones
- Overlay con render del PDF original.
- Calibración.
- Unión/deduplicación.
- Curvas.
- Detección de muros.

## Criterios de aceptación
- [x] PDF vectorial controlado se marca compatible.
- [x] PDF raster controlado se marca no compatible.
- [x] Coordenadas de segmentos se conservan.
- [x] Rectángulo se descompone en 4 segmentos.
- [x] API upload→geometry funciona end-to-end.
- [x] Frontend de revisión implementado en código.
- [x] Build frontend verificado en entorno con acceso a npm.
- [x] Validación con al menos un PDF arquitectónico real del usuario.

## Validación real y cierre

- PDF validado mediante el flujo de la aplicación: `samples/PLANO PDF LEO.pdf`.
- Preflight compatible: 1 página, 5176 paths, 11148 segmentos, 2 imágenes, 100 bloques de texto y 124 elementos vectoriales no convertidos.
- `POST /api/documents` respondió `201 Created`; `GET /api/documents/{id}/geometry?page=1` respondió `200 OK` con la geometría de la página.
- El build frontend está registrado como PASS en `STATUS.md` y T-012 está completada; se volvió a ejecutar para este cierre.
- La validación cubre extracción de geometría recta y rectángulos. No valida curvas, identificación semántica de vistas ni detección de muros.
- No fue necesario repetir la prueba móvil de F00-H02 para satisfacer los criterios de este hito.
