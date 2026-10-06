# F00-H02 — Plan

```text
Android / navegador PC
        │ :8080
        ▼
      Nginx
      ├── /      → frontend estático
      └── /api/  → backend:8000
                     │
                     ▼
                  FastAPI
```

El frontend se construye con `VITE_API_BASE=/api`; de esta forma la URL del PC no se codifica en el bundle y la misma imagen sirve tanto en localhost como en la IP LAN.

El backend no se publica directamente hacia el teléfono en Compose. Nginx es el único puerto de entrada.
