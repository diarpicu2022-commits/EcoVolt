# EcoVolt – Frontend

Frontend del sistema de energía solar inteligente, construido en **Python** con [Flet](https://flet.dev).

## Estructura del proyecto

```
frontend/
├── main.py                  # Punto de entrada
├── requirements.txt         # Dependencias
├── .env                     # Variables de entorno (no subir a git)
├── config/
│   └── settings.py          # Configuración centralizada
├── services/
│   ├── auth_service.py      # Autenticación JWT
│   ├── energy_service.py    # Llamadas a la API REST
│   └── websocket_service.py # Conexión WebSocket en tiempo real
├── components/
│   ├── metric_card.py       # Tarjeta de KPI reutilizable
│   ├── device_card.py       # Tarjeta de dispositivo IoT
│   ├── battery_gauge.py     # Indicador circular de batería
│   └── navbar.py            # Barra de navegación superior
└── views/
    ├── login_view.py        # Pantalla de login / registro
    └── dashboard_view.py    # Panel principal de monitoreo
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
flet run main.py
```

## Variables de entorno

Copia `.env` y ajusta los valores:

| Variable        | Descripción                        | Default                  |
|-----------------|------------------------------------|--------------------------|
| `API_BASE_URL`  | URL base del backend FastAPI       | `http://localhost:8000`  |
| `API_V1_STR`    | Prefijo de la API                  | `/api/v1`                |
| `WS_BASE_URL`   | URL base para WebSocket            | `ws://localhost:8000`    |
