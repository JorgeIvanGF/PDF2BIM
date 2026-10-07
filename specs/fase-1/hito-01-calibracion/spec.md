# F01-H01 — Calibración PDF → milímetros

**Estado:** CERRADO

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
- [x] Validación manual con una cota de plano real.

## Validación real y cierre

- PDF validado: `samples/PLANO PDF LEO.pdf`, cota horizontal inferior `13,35` de la primera planta.
- La unidad de la cota no está declarada en el PDF. Para esta validación, el usuario confirmó interpretarla como 13,35 m = 13350 mm.
- El usuario confirmó que ambos puntos se seleccionaron en los extremos de la cota y que el contador de la interfaz llegó a `2/2`.
- Punto A: `(274.9101868, 1539.3955078)` unidades PDF; punto B: `(1031.5212402, 1539.3955078)` unidades PDF.
- Distancia euclídea: `756.6110535` unidades PDF. Con la fórmula documentada, el factor es `17.6444686 mm/unidad PDF`.
- La prueba automatizada `tests/test_calibration.py` pasó.
- Esta evidencia valida la calibración mediante dos puntos con una cota real. No valida normalización geométrica ni detección de muros.
