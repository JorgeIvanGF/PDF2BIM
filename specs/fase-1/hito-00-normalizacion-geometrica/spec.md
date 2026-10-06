# F01-H00 — Normalización geométrica

**Estado:** EN VALIDACIÓN (implementación provisional sobre fixtures)

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
- [ ] Validación sobre geometría de plano arquitectónico real.
