# Verificación tecnológica — 2026-10-05

- React 19.3 es la versión estable documentada por React en octubre de 2026.
- Vite mantiene Vite 8 como línea estable y publica parches actuales en la rama 8.x.
- PyMuPDF expone `Page.get_drawings()` para recuperar paths vectoriales.
- That Open mantiene documentación activa para su arquitectura de Components.

Las dependencias del prototipo se expresan con rangos compatibles; el lockfile deberá generarse en el entorno de desarrollo con acceso al registro npm/PyPI.

## Actualización de compatibilidad frontend

Se alineó el prototipo con las versiones publicadas/verificadas el 2026-10-05:
- `@thatopen/components` 3.4.8
- `@thatopen/components-front` 3.4.4
- `@thatopen/fragments` 3.4.7
- `three` 0.184.0 (compatible con peer `>=0.182.0` y coincidente con el entorno de desarrollo del repositorio de That Open consultado)
- `camera-controls` 3.1.2
- `web-ifc` 0.0.77
- `pdfjs-dist` 6.3.289

El build efectivo continúa pendiente porque el entorno actual no logró completar `npm install` antes del timeout de red. Esta limitación se registra como validación pendiente, no como fallo funcional probado.
