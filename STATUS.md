# Estado técnico — 2026-10-05 — hotfix 0.1.1

## Resultado verificable

- Backend: **14/14 pruebas pasan** con Python 3.14 en entorno virtual.
- Compilación Python: correcta (`compileall`).
- Flujo probado: PDF sintético → preflight → segmentos raw → normalización → calibración → `WallCandidate`.
- Fixture `samples/plano-prueba-vectorial-01.pdf` procesado por la API con calibración 17.638 mm/unidad: **6 candidatos**, cuatro de 200 mm y dos de 100 mm.
- Frontend implementado: carga, diagnóstico, render del PDF original con PDF.js, overlay SVG, calibración táctil, detección, exportación JSON y visor 3D preliminar con That Open Engine.
- Infraestructura local/móvil implementada: Docker Compose + Nginx reverse proxy, puerto único `8080`.
- Build frontend local: **PASS** (`tsc -b` y Vite 8.3.2); los errores TS7016 y TS5096 no reaparecen. Se generó `frontend/package-lock.json` para fijar el árbol instalado.
- Docker Compose: la imagen backend construye; la imagen web no pudo iniciar porque el daemon Docker no resolvió `registry-1.docker.io` para las imágenes base `node:24-alpine` y `nginx:1.29-alpine`.
- No se pudieron verificar los contenedores en ejecución, el proxy `/api`, `http://localhost:8080` ni el acceso móvil.

## Estado SDD

- F00-H00 Fundamentos/arquitectura: **CERRADO**.
- F00-H01 Extracción vectorial: **EN VALIDACIÓN**; falta plano real.
- F00-H02 Entorno de ejecución/prueba móvil: **EN VALIDACIÓN**; la compilación local del frontend pasa. El build integral de Docker está bloqueado por resolución DNS de Docker Hub; faltan prueba de proxy, navegador PC y Android.
- F01-H00 Normalización: **EN VALIDACIÓN provisional**.
- F01-H01 Calibración: **EN VALIDACIÓN provisional**; UI táctil implementada.
- F01-H02 Overlay PDF + geometría: **EN VALIDACIÓN técnica / pendiente validación visual con PDF real**; build frontend verificado.
- F02-H00 Detector inicial de muros: **EN VALIDACIÓN provisional**.
- F03-H00 Visor 3D: **EN VALIDACIÓN técnica / pendiente navegador y gestos Android**; build frontend verificado.

## Bloqueos y pendientes

Para cerrar la primera cadena de validación hace falta **un PDF arquitectónico vectorial real representativo del uso previsto**. También hace falta un entorno donde Docker pueda descargar las imágenes base y probar el flujo de PC/móvil.

## Riesgos abiertos

1. El detector inicial compara pares O(n²); se optimizará después de perfilar un plano real.
2. Solo soportamos segmentos rectos y rectángulos; curvas se registran, no se reinterpretan.
3. El overlay PDF.js + SVG está implementado, pero aún deben verificarse alineación, rotación y CropBox con un plano real.
4. La clasificación 100/200 mm es configurable y no implica todavía interior/exterior.
5. El 3D es de validación geométrica, no un BIM/IFC formal.
6. El build frontend quedó verificado localmente; la imagen web y el flujo Compose quedan sin verificar hasta que Docker Hub sea resoluble desde el daemon.

## Git

- El directorio recibido no tenía `.git`; la auditoría confirmó que el remoto oficial no contiene referencias.
- Se inicializó la historia local en `main` y se configuró `origin` al repositorio oficial.
- Los fixtures PDF deliberados están versionados; `node_modules/`, `.venv/`, `dist/`, cachés y variables locales están excluidos por `.gitignore`.
