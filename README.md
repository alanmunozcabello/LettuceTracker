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