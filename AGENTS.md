# AGENTS.md — PDF2BIM

## Metodología obligatoria
El proyecto usa Specification Driven Development (SDD) por fases e hitos.

Ciclo: DEFINIR → DISEÑAR → IMPLEMENTAR → PROBAR → ANALIZAR → DOCUMENTAR → CONTINUAR.

Antes de implementar funcionalidad significativa:
1. `spec.md` debe definir alcance, exclusiones y aceptación.
2. `plan.md` debe describir diseño y verificación.
3. `tasks.md` debe contener tareas verificables.

No adelantar lógica de fases futuras salvo contratos mínimos que eviten retrabajo.

## Principios arquitectónicos
- El lector PDF no depende de Revit.
- El dominio geométrico no depende de PyMuPDF.
- Revit, IFC, IA y MCP son consumidores/capas posteriores.
- Las coordenadas originales del PDF se conservan para overlays exactos.
- La geometría BIM futura trabajará en unidades reales; la calibración pertenece a Fase 1.
- Ante ambigüedad, marcar para revisión; no inventar semántica BIM.

## Stack inicial
- Backend: Python, FastAPI, Pydantic, PyMuPDF.
- Geometry: Python; Shapely/NumPy cuando aporten valor claro.
- Frontend: React, TypeScript, Vite.
- PDF web: PDF.js.
- 3D futuro: Three.js + That Open Engine.
- Tests backend: pytest.
- Tests frontend: Vitest + Playwright cuando el entorno Node esté disponible.

## Calidad
- Código tipado cuando aplique.
- Funciones geométricas puras siempre que sea posible.
- Cada bug geométrico reproducible debe terminar como fixture o prueba de regresión.
- No introducir base de datos en el MVP inicial.
