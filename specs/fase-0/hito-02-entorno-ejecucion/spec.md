# F00-H02 — Entorno de ejecución y prueba móvil

**Estado:** CERRADO

## Objetivo
Definir un camino reproducible para ejecutar PDF2BIM en un PC y probar la interfaz desde un teléfono conectado a la misma red local, sin exigir APK ni despliegue cloud.

## Alcance
- Contenedor backend FastAPI.
- Build estático del frontend con Vite.
- Nginx como servidor web y reverse proxy `/api`.
- Docker Compose con puerto único `8080` hacia el navegador.
- Configuración del frontend con `VITE_API_BASE=/api` para funcionamiento same-origin.

## Criterios de aceptación
1. `docker compose up --build` construye ambos servicios en un entorno con acceso a PyPI/npm.
2. `http://localhost:8080` abre la aplicación desde el PC.
3. `http://<IP-LAN-PC>:8080` abre la aplicación desde un teléfono en la misma red.
4. La carga de PDF llega al backend a través del reverse proxy.
5. No se requiere CORS para el flujo servido por Nginx.

## Resultado de validación

Los cinco criterios se cumplieron. El criterio 3 se registra según la prueba móvil reportada por el usuario: la aplicación y `/api/health` respondieron correctamente en `http://192.168.20.183:8080`; el modelo, sistema operativo y navegador del dispositivo no fueron informados.

## Exclusiones
- HTTPS público.
- Dominio propio.
- Autenticación.
- Hosting permanente.
- APK/PWA instalable.
