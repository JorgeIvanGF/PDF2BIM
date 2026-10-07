# F01-H00 — Normalización geométrica

**Estado:** CERRADO

## Objetivo
Convertir `Segment2D` crudos en segmentos canónicos aptos para cálculo geométrico, sin introducir todavía semántica arquitectónica.

## Alcance implementado
- Descartar segmentos degenerados.
- Canonicalizar sentido de extremos.
- Calcular longitud en unidades PDF.
- Calcular ángulo normalizado `[0, 180)`.
- Colapsar duplicados exactos/invertidos conservando trazabilidad de IDs fuente.

## Decisión revisada
La unión aproximada de segmentos colineales se pospone hasta disponer de calibración real. No se introducirán tolerancias arquitectónicas expresadas en unidades PDF arbitrarias.

## Exclusiones
- Clasificación de muros.
- Merge colineal con gap.
- Tolerancias en milímetros.

## Aceptación
- [x] Duplicado invertido se colapsa.
- [x] Trazabilidad de ambos segmentos fuente se conserva.
- [x] Segmento degenerado se elimina.
- [x] Longitud y ángulo quedan calculados.
- [x] Validación sobre geometría de plano arquitectónico real.

## Validación real y cierre

- PDF validado: `samples/PLANO PDF LEO.pdf`. Se ejecutaron el lector y el normalizador existentes sobre la geometría vectorial de la página completa.
- Resultado: 11148 segmentos extraídos, 10360 normalizados, 103 degenerados eliminados, 606 grupos con duplicados y 685 duplicados colapsados.
- Se preservaron 11045 IDs fuente tras eliminar degenerados. No se encontraron inconsistencias de canonicalización, longitud o ángulo.
- `backend/tests/test_normalize.py`: 2 pruebas pasadas.
- La lámina contiene varias vistas; la normalización se validó sobre la página completa y no atribuye semántica de muro a sus segmentos.
- Esta evidencia no valida elementos curvos que no se convierten a segmentos ni la detección de muros de F02-H00.
