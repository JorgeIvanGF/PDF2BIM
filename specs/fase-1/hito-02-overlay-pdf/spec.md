# F01-H02 — Overlay PDF + geometría

**Estado:** CERRADO

## Objetivo
Renderizar la página PDF original en navegador y superponer exactamente la geometría extraída usando un SVG con el mismo sistema de coordenadas lógico.

## Alcance
- PDF.js renderiza la página 1 desde el `File` local ya seleccionado por el usuario.
- Canvas PDF y SVG geométrico comparten el mismo contenedor y relación de aspecto.
- Selección táctil de puntos se realiza sobre el SVG.
- Segmentos raw, puntos de calibración y ejes de muros se muestran como capas.

## Exclusiones
- Multi-página interactiva.
- Rotaciones/cropboxes exóticos verificados con fixtures reales.
- Edición geométrica directa.

## Aceptación
- [x] Componente PDF.js implementado.
- [x] SVG transparente superpuesto al canvas.
- [x] Click/touch sigue produciendo coordenadas PDF2BIM.
- [x] Build frontend.
- [x] Validación visual con PDF real.

## Validación real y cierre

- PDF validado: `samples/PLANO PDF LEO.pdf` (una página, varias vistas en la misma lámina).
- El backend extrajo 11148 segmentos y la lámina renderizó correctamente en PDF.js.
- El usuario confirmó que el overlay SVG coincide visualmente con el PDF en la primera planta, incluidos muros exteriores e interiores y líneas relevantes.
- El usuario confirmó que los puntos quedan donde se hace clic y que la selección de dos puntos llega a `2/2`.
- La validación se limita al render, alineación y selección de puntos de F01-H02. No valida la normalización, la calibración real ni la detección/clasificación de muros de otros hitos.
- La lámina contiene varias vistas; los segmentos extraídos pertenecen a la página completa y no se interpretan todos como muros de la primera planta.
