# F00-H00 — Plan

## Arquitectura
Monolito modular con frontend y backend separados por HTTP/JSON.

```text
frontend ─HTTP─> backend
                 ├─ pdf/
                 ├─ geometry/
                 ├─ interpreter/ (futuro)
                 └─ services/
```

## Principios
- Dependency direction: dominio geométrico no importa PyMuPDF.
- Revit nunca será requisito para ejecutar el motor PDF.
- Fixtures controlados antes de planos reales complejos.
- SDD precede funcionalidad significativa.

## Riesgos iniciales
- PDFs que convierten trazos simples en curvas/paths complejos.
- Duplicación de geometría debida a rellenos/hachurados.
- Transformaciones de página y recortes.

## Mitigación
F00-H01 se limita a demostrar extracción; F01 normalizará y resolverá ruido.
