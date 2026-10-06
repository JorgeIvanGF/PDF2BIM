# ADR-001 — Stack inicial

**Estado:** Aceptado

## Decisión
Backend en Python/FastAPI/PyMuPDF; frontend React/TypeScript/Vite; 3D posterior con Three.js/That Open Engine.

## Razón
Python reduce fricción para geometría y PDF. React/TS ofrece una UI web móvil reutilizable. El 3D web desacopla la validación de Revit.

## Consecuencia
Habrá un contrato JSON explícito entre frontend y backend.
