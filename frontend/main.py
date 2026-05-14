from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config.settings import settings
from services.energy_service import energy_service


BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(
    title=settings.APP_TITLE,
    description="EcoVolt solar monitoring frontend",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def build_template_context(request: Request, page_name: str, payload: dict) -> dict:
    # Centraliza el contexto para mantener consistencia entre vistas.
    return {
        "request": request,
        "app_title": settings.APP_TITLE,
        "navigation_items": settings.navigation_items,
        "current_page": page_name,
        "payload": payload,
    }


@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request) -> HTMLResponse:
    payload = await energy_service.get_dashboard_payload()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=build_template_context(request, "dashboard", payload),
    )


@app.get("/paneles", response_class=HTMLResponse)
async def panels_page(request: Request) -> HTMLResponse:
    payload = await energy_service.get_panels_payload()
    return templates.TemplateResponse(
        request=request,
        name="panels.html",
        context=build_template_context(request, "paneles", payload),
    )


@app.get("/baterias", response_class=HTMLResponse)
async def batteries_page(request: Request) -> HTMLResponse:
    payload = await energy_service.get_batteries_payload()
    return templates.TemplateResponse(
        request=request,
        name="batteries.html",
        context=build_template_context(request, "baterias", payload),
    )


@app.get("/cargas", response_class=HTMLResponse)
async def loads_page(request: Request) -> HTMLResponse:
    payload = await energy_service.get_loads_payload()
    return templates.TemplateResponse(
        request=request,
        name="loads.html",
        context=build_template_context(request, "cargas", payload),
    )


@app.get("/alertas", response_class=HTMLResponse)
async def alerts_page(request: Request) -> HTMLResponse:
    payload = await energy_service.get_alerts_payload()
    return templates.TemplateResponse(
        request=request,
        name="alerts.html",
        context=build_template_context(request, "alertas", payload),
    )


@app.get("/api/dashboard", response_class=JSONResponse)
async def dashboard_api() -> JSONResponse:
    return JSONResponse(await energy_service.get_dashboard_payload())


@app.get("/api/panels", response_class=JSONResponse)
async def panels_api() -> JSONResponse:
    return JSONResponse(await energy_service.get_panels_payload())


@app.get("/api/batteries", response_class=JSONResponse)
async def batteries_api() -> JSONResponse:
    return JSONResponse(await energy_service.get_batteries_payload())


@app.get("/api/loads", response_class=JSONResponse)
async def loads_api() -> JSONResponse:
    return JSONResponse(await energy_service.get_loads_payload())


@app.get("/api/alerts", response_class=JSONResponse)
async def alerts_api() -> JSONResponse:
    return JSONResponse(await energy_service.get_alerts_payload())


if __name__ == "__main__":
    # Permite ejecutar la app directamente durante desarrollo local.
    uvicorn.run("main:app", host="127.0.0.1", port=8501, reload=True)
