# F01-H01 — Calibración PDF → milímetros

**Estado:** EN VALIDACIÓN (implementación provisional sobre fixtures)

## Objetivo
Obtener un factor reproducible que convierta distancias del sistema de coordenadas PDF en milímetros reales a partir de dos puntos elegidos y una distancia conocida.

## Fórmula
`mm_per_pdf_unit = real_distance_mm / distance(pointA, pointB)`

## Alcance
- Dos puntos PDF distintos.
- Distancia real positiva.
- Resultado explícito y reutilizable en análisis posteriores.

## Exclusiones
- Lectura automática de escala 1:N.
- Detección automática de cotas.

## Aceptación
- [x] Caso 3-4-5 produce factor exacto esperado.
- [x] Puntos coincidentes son inválidos.
- [ ] Validación manual con una cota de plano real.
