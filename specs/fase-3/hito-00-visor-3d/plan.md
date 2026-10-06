# F03-H00 — Plan

## Diseño
That Open Engine gestiona escena, renderer y cámara. Los muros preliminares son `THREE.Mesh` agregados a `world.scene.three`.

```text
WallCandidate (mm)
  ↓ /1000
prisma Three.js (m)
  ↓
That Open World
  ↓
WebGL navegador
```

## Coordenadas
- X PDF/BIM → X Three.js.
- Y PDF/BIM → Z Three.js invertido para vista de planta intuitiva.
- Altura → Y Three.js.
- El conjunto se recentra por bounding box de ejes.

## Limpieza
El componente React llama `components.dispose()` al desmontarse, siguiendo el contrato `Disposable` de That Open Engine.
