# F02-H00 — Detector geométrico inicial de muros

**Estado:** EN VALIDACIÓN (implementación provisional sobre fixtures)

## Objetivo
Detectar un primer `WallCandidate` cuando dos segmentos normalizados representan caras aproximadamente paralelas de un muro y su separación coincide con una regla de espesor configurada.

## Entradas
- `NormalizedSegment2D[]`
- calibración mm/unidad PDF
- `WallTypeRule[]`
- tolerancia angular
- solapamiento mínimo absoluto y relativo

## Reglas del MVP
1. Las líneas deben ser aproximadamente paralelas.
2. Deben solaparse longitudinalmente.
3. El solapamiento debe superar mínimo absoluto y ratio configurado.
4. La distancia perpendicular debe coincidir con al menos un tipo de muro.
5. El eje se calcula en la mitad de ambas caras dentro del tramo solapado.
6. La confianza es un índice geométrico determinista, no una probabilidad estadística.

## Exclusiones
- Semántica interior/exterior automática.
- Encuentros L/T/X.
- Puertas/ventanas.
- Curvas.
- Optimización espacial para miles de segmentos.

## Aceptación
- [x] Detecta muro horizontal de 200 mm controlado.
- [x] Calcula eje central correcto.
- [x] Rechaza espesor no configurado.
- [x] Rechaza líneas sin solapamiento.
- [x] Endpoint end-to-end desde PDF sintético.
- [ ] Validación de falsos positivos sobre plano real.
