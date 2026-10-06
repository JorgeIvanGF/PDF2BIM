# F03-H00 — Visor 3D preliminar con That Open Engine

**Estado:** EN IMPLEMENTACIÓN / pendiente de build frontend

## Objetivo
Visualizar los `WallCandidate` detectados como prismas 3D navegables en navegador, sin generar todavía un modelo IFC/Revit.

## Alcance
- Mundo 3D de That Open Engine.
- Geometría Three.js añadida al mundo.
- Altura global configurable; default 2700 mm.
- Longitud y espesor derivados del `WallCandidate`.
- Centrado del modelo alrededor del origen para mejorar navegación.
- Cámara inicial orientada al conjunto.
- Soporte mouse/touch proporcionado por el control de cámara.

## Exclusiones
- IFC.
- Propiedades BIM formales.
- Edición 3D.
- Selección semántica individual.
- Revit.

## Aceptación
- [x] Componente React implementado.
- [x] Cada `WallCandidate` produce un prisma con largo/espesor correctos en metros.
- [x] Se libera `Components` al desmontar React.
- [ ] Build verificado con dependencias npm.
- [ ] Navegación validada en Android.
