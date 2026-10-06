# F01-H02 — Overlay PDF + geometría

**Estado:** EN IMPLEMENTACIÓN / pendiente de build frontend

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
- [ ] Build frontend.
- [ ] Validación visual con PDF real.
