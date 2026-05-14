# EcoVolt - Frontend Web

Frontend web del sistema de energia solar inteligente, construido con **FastAPI + Jinja2 + HTML/CSS/JS**.

## Caracteristicas

- Dashboard responsive con tema solar
- Vistas para paneles, baterias, cargas y alertas
- Polling automatico cada 5 segundos
- Datos mock de respaldo para trabajar aunque el backend aun no este completo

## Ejecucion

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8501
```

Luego abre `http://127.0.0.1:8501`.

## Variables de entorno

| Variable | Descripcion | Default |
|---|---|---|
| `API_BASE_URL` | URL base del backend | `http://localhost:8000` |
| `API_V1_STR` | Prefijo de la API | `/api/v1` |
| `WS_BASE_URL` | URL base de websocket | `ws://localhost:8000` |
