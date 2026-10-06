# F00-H00 — Fundamentos y arquitectura

**Estado:** CERRADO

## Objetivo
Definir el marco de trabajo SDD, límites del MVP, arquitectura desacoplada y stack inicial de PDF2BIM.

## Alcance
- Metodología por fases/hitos.
- Stack frontend/backend.
- Separación PDF Reader → Geometry Domain → intérprete futuro.
- Estrategia de pruebas.
- Estructura del repositorio.

## Exclusiones
- Detección de muros.
- Revit, IFC, MCP e IA.
- Persistencia de usuarios/proyectos.

## Decisiones
1. PDF vectorial primero; raster fuera del MVP.
2. PyMuPDF como extractor del backend.
3. React/TypeScript/Vite para UI.
4. That Open Engine reservado al 3D de una fase posterior.
5. Sin base de datos inicialmente.
6. Las coordenadas PDF se conservan intactas hasta la calibración.

## Criterios de aceptación
- [x] Estructura SDD definida.
- [x] Stack definido.
- [x] Límites arquitectónicos documentados.
- [x] Estructura inicial de repo definida.
- [x] Reglas del proyecto consolidadas en `AGENTS.md`.
