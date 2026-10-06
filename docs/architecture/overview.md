# Arquitectura PDF2BIM

## Boundary map

```text
PDF bytes
  ↓
PDF Adapter (PyMuPDF)
  ↓
Raw geometry contracts
  ↓
Geometry normalization
  ↓
Architectural interpretation
  ↓
Intermediate BIM domain
  ├─ 2D review
  ├─ 3D review / That Open Engine
  ├─ IFC
  └─ Revit connector
```

## Regla principal
Ninguna capa anterior puede depender de una salida concreta como Revit. Esto permite validar el núcleo de interpretación sin Autodesk instalado.
