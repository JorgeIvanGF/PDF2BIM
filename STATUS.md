# Estado técnico — 2026-10-06 — hotfix 0.1.1

## Resultado verificable

- Backend: **14/14 pruebas pasan** con Python 3.14 en entorno virtual.
- Compilación Python: correcta (`compileall`).
- Flujo probado: PDF sintético → preflight → segmentos raw → normalización → calibración → `WallCandidate`.
- Fixture `samples/plano-prueba-vectorial-01.pdf` procesado por la API con calibración 17.638 mm/unidad: **6 candidatos**, cuatro de 200 mm y dos de 100 mm.
- Frontend implementado: carga, diagnóstico, render del PDF original con PDF.js, overlay SVG, calibración táctil, detección, exportación JSON y visor 3D preliminar con That Open Engine.
- **PASADO:** F01-H02 validado con `samples/PLANO PDF LEO.pdf`; backend extrajo 11148 segmentos y el usuario confirmó render correcto, alineación visual del overlay en primera planta y selección de dos puntos hasta `2/2`.
- **PASADO:** F00-H01 validado con `samples/PLANO PDF LEO.pdf` en el flujo de la aplicación: preflight compatible (1 página, 5176 paths, 11148 segmentos, 2 imágenes, 100 bloques de texto, 124 elementos no convertidos), upload `201 Created` y consulta de geometría `200 OK`. El build frontend pasó. La validación cubre segmentos rectos y rectángulos, no curvas, semántica de vistas ni detección de muros.
- **PASADO:** F01-H00 validado con `samples/PLANO PDF LEO.pdf`; 11148 segmentos extraídos, 10360 normalizados, 103 degenerados eliminados, 685 duplicados colapsados y 11045 IDs fuente preservados; invariantes de canonicalización, longitud y ángulo sin inconsistencias. Pruebas de normalización: 2/2.
- Infraestructura local/móvil implementada: Docker Compose + Nginx reverse proxy, puerto único `8080`.
- Build frontend local: **PASS** (`tsc -b` y Vite 8.3.2); los errores TS7016 y TS5096 no reaparecen. Se generó `frontend/package-lock.json` para fijar el árbol instalado.
- **PASADO:** Docker Desktop 4.35.1 / Engine 27.3.1 responden con permisos elevados; Compose 2.29.7.
- **PASADO:** `docker compose up --build -d` construye ambos servicios, accede a Docker Hub e inicia los contenedores.
- **PASADO:** `http://localhost:8080` responde 200 y la interfaz se carga en Chrome.
- **PASADO:** `/api/health` devuelve `status=ok`; la interfaz carga el fixture y consulta geometría vía `/api` same-origin (9 segmentos), sin requerir CORS.
- **FALLIDO, CORREGIDO Y REVERIFICADO:** Nginx servía el worker `.mjs` como `application/octet-stream`, lo que impedía su importación. Ahora devuelve `application/javascript` y PDF.js renderiza el canvas 1053×744 sin mensaje de error.
- **PASADO EN EL HOST:** `192.168.20.183:8080` responde 200 desde este PC y Docker publica el puerto en `0.0.0.0`.
- **BLOQUEADO:** ninguno actualmente por dependencias externas; el fallo DNS previo de Docker Hub no se reprodujo.
- **PASADO, reportado por el usuario:** desde un teléfono en la misma Wi-Fi, `http://192.168.20.183:8080` cargó y `/api/health` respondió `status: ok`. Modelo, SO y navegador no informados.

## Estado SDD

- **F00-H02 está cerrado** tras completar sus cinco criterios de aceptación.
- No se inicia otro hito en esta intervención, según la instrucción del usuario.

- F00-H00 Fundamentos/arquitectura: **CERRADO**.
- F00-H01 Extracción vectorial: **CERRADO**; criterios sintéticos, build y flujo real con PDF arquitectónico satisfechos. No valida curvas, identificación semántica de vistas ni detección de muros.
- F00-H02 Entorno de ejecución/prueba móvil: **CERRADO**; cinco criterios cumplidos. La validación desde teléfono se registra como reportada por el usuario.
- F01-H00 Normalización: **CERRADO**; criterios automatizados y validación sobre geometría de plano arquitectónico real satisfechos. No valida curvas ni detección de muros.
- F01-H01 Calibración: **CERRADO**; prueba automatizada y validación manual con cota real satisfechas. El usuario confirmó 13350 mm, puntos de la cota `13,35` y selección `2/2`; factor obtenido: 17.6444686 mm/unidad PDF. Esto no valida F02-H00.
- F01-H02 Overlay PDF + geometría: **CERRADO**; aceptación de build y validación real satisfechas. La evidencia cubre únicamente render, alineación y selección de puntos de este hito.
- F02-H00 Detector inicial de muros: **EN VALIDACIÓN provisional**.
- F03-H00 Visor 3D: **EN VALIDACIÓN técnica / pendiente navegador y gestos Android**; build frontend verificado.

## Bloqueos y pendientes

F00-H02 y F00-H01 no tienen pendientes abiertos. F02-H00 continúa en validación independiente; su cierre no forma parte de la evidencia de extracción registrada aquí.

## Riesgos abiertos

1. El detector inicial compara pares O(n²); se optimizará después de perfilar un plano real.
2. Solo soportamos segmentos rectos y rectángulos; curvas se registran, no se reinterpretan.
3. El overlay PDF.js + SVG quedó validado visualmente con `samples/PLANO PDF LEO.pdf`; rotaciones y CropBoxes exóticos siguen fuera del alcance verificado.
4. La clasificación 100/200 mm es configurable y no implica todavía interior/exterior.
5. El 3D es de validación geométrica, no un BIM/IFC formal.
6. El worker PDF.js `.mjs` requiere MIME JavaScript en Nginx; se corrigió y verificó en el stack.

## Git

- El directorio recibido no tenía `.git`; la auditoría confirmó que el remoto oficial no contiene referencias.
- Se inicializó la historia local en `main` y se configuró `origin` al repositorio oficial.
- Los fixtures PDF deliberados están versionados; `node_modules/`, `.venv/`, `dist/`, cachés y variables locales están excluidos por `.gitignore`.
