from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import random
import sys

# Asegurar que el directorio actual esté en el path para las importaciones
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / "backend"))

# Importar clases reales de dominio
try:
    from domain.entities.monocrystalline_panel import MonocrystallinePanel
    from domain.entities.lithium_battery import LithiumBattery
    from data_structures.arrays.solar_panel_dynamic_array import SolarPanelDynamicArray
    from patterns.structural.chart_renderer import ChartData
    from patterns.structural.json_chart_renderer import JsonChartRenderer
except ImportError as e:
    print(f"Error al importar clases de dominio o patrones: {e}")
    # Fallback si las importaciones fallan
    MonocrystallinePanel = None
    LithiumBattery = None
    SolarPanelDynamicArray = None
    ChartData = None
    JsonChartRenderer = None

app = FastAPI(title="EcoVolt - Sistema de Energía Solar")

# Inicializar renderizador de gráficos (Patrón Bridge)
chart_renderer = JsonChartRenderer() if JsonChartRenderer else None

# Configurar CORS para permitir solicitudes desde cualquier origen en el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción debe ser más restrictivo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos y templates
static_dir = BASE_DIR / "frontend" / "static"
templates_dir = BASE_DIR / "frontend" / "templates"
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

# Inicializar estado del sistema con clases reales
system_panels = SolarPanelDynamicArray() if SolarPanelDynamicArray else None
if system_panels:
    system_panels.append("MONO-001")
    system_panels.append("MONO-002")

main_battery = LithiumBattery(
    component_id="BATT-CORE",
    installation_location="Cuarto de Control",
    installation_date="2026-01-10",
    battery_id="LI-CORE-01",
    capacity_kwh=15.5
) if LithiumBattery else None

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

# API Metrics con integración de lógica real y Patrón Bridge
@app.get("/api/v1/metrics")
async def get_metrics():
    # Usar datos reales de la batería si existe
    bat_lvl = main_battery._current_charge_percentage if main_battery else random.randint(15, 95)
    
    # Preparar datos del gráfico usando el Patrón Bridge (JsonChartRenderer)
    chart_json = {}
    if ChartData and chart_renderer:
        data = ChartData(
            chart_title="Producción vs Consumo (kW)",
            labels=["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"],
            values=[2.5, 3.8, 5.2, 6.8, 6.2, 4.5],
            chart_type="line"
        )
        # El renderizador produce una cadena JSON
        chart_json = json.loads(chart_renderer.render(data))
    
    return {
        "solar_gen": round(random.uniform(2.0, 7.0), 2),
        "battery_lvl": bat_lvl,
        "energy_cons": round(random.uniform(1.0, 4.0), 2),
        "status": "online",
        "panel_count": system_panels.size() if system_panels else 0,
        # Gráfica renderizada vía Bridge
        "chart_data": chart_json
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
