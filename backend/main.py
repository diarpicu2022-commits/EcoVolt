from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(title="EcoVolt - Sistema de Energía Solar")

# Obtener la ruta del directorio base (EcoVolt/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurar archivos estáticos y templates
# Asegurarse de que las carpetas existan
static_dir = BASE_DIR / "frontend" / "static"
templates_dir = BASE_DIR / "frontend" / "templates"
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "title": "Dashboard - EcoVolt"})

@app.get("/paneles")
async def panels(request: Request):
    return templates.TemplateResponse("paneles.html", {"request": request, "title": "Paneles Solares - EcoVolt"})

@app.get("/baterias")
async def batteries(request: Request):
    return templates.TemplateResponse("baterias.html", {"request": request, "title": "Baterías - EcoVolt"})

@app.get("/consumo")
async def consumption(request: Request):
    return templates.TemplateResponse("consumo.html", {"request": request, "title": "Consumo y Cargas - EcoVolt"})

@app.get("/alertas")
async def alerts(request: Request):
    return templates.TemplateResponse("alertas.html", {"request": request, "title": "Alertas del Sistema - EcoVolt"})

# API Mock Endpoints para el polling del frontend
@app.get("/api/v1/metrics")
async def get_metrics():
    import random
    return {
        "solar_gen": round(random.uniform(2.0, 7.0), 2),
        "battery_lvl": random.randint(15, 95),
        "energy_cons": round(random.uniform(1.0, 4.0), 2),
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
