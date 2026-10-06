# F02-H00 — Plan

## Algoritmo
Implementación correctness-first por comparación de pares.

Complejidad actual: O(n²). No se optimiza todavía porque primero necesitamos perfilar un plano real y conocer distribución de segmentos. Si el preprocesado supera ~2500 segmentos se emite advertencia.

## Confianza
Ponderación inicial:
- 35% paralelismo
- 40% proximidad al espesor nominal
- 25% proporción de solapamiento

Estos pesos son heurísticos explícitos y deberán recalibrarse con fixtures reales.
