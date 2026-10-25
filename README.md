# LettuceTracker
Proyecto de curso Diseño de Software

Integrantes:

## Instrucciones

### Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Ejecutar la API

Desde la carpeta raíz del proyecto:

```bash
uvicorn src.app:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

### Ejecutar las pruebas

```bash
python3 -m pytest -q
```

La documentación interactiva está disponible en `http://127.0.0.1:8000/docs`.

### Login provisional

El formulario está disponible en `http://127.0.0.1:8000/static/html/login.html`.
El endpoint `POST /api/v1/auth/login` valida el correo y la contraseña contra
`src/data/usuarios.json`. Esta versión es únicamente para el avance del
proyecto: las contraseñas se almacenan y comparan en texto plano, no se crean
sesiones persistentes, y esta implementación debe reemplazarse antes de usar
el sistema en producción.

El login crea un JWT con una duración máxima de 4 horas en una cookie
`HttpOnly`. El dashboard valida esa cookie en el servidor y el botón **Salir**
la elimina. La clave de firma se puede configurar con la variable de entorno
`LETTUCE_JWT_SECRET`; el valor incluido en el código es solo para desarrollo
local.