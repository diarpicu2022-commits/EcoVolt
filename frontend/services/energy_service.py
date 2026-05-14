from __future__ import annotations

import math
from datetime import datetime, timedelta


class EnergyService:
    def _build_panels(self) -> list[dict]:
        current_hour = datetime.now().hour + (datetime.now().minute / 60)
        daylight_factor = max(0.18, math.sin(((current_hour - 6) / 12) * math.pi))
        panel_blueprints = [
            ("PV-01", "Monocristalino Norte", 96.2, 42.4, 9.1, 27.4, "Activo"),
            ("PV-02", "Monocristalino Este", 94.8, 40.7, 8.8, 28.1, "Activo"),
            ("PV-03", "Pelicula Delgada Sur", 88.5, 32.2, 7.4, 30.6, "En espera"),
            ("PV-04", "Policristalino Oeste", 91.6, 36.9, 8.2, 29.7, "Mantenimiento"),
        ]

        panels: list[dict] = []
        for index, blueprint in enumerate(panel_blueprints, start=1):
            panel_id, name, efficiency, base_voltage, base_current, base_temp, status = blueprint
            modulation = 0.82 + (daylight_factor * (0.16 + index * 0.02))
            power = round(base_voltage * base_current * modulation / 100, 2)
            panels.append(
                {
                    "id": panel_id,
                    "name": name,
                    "status": status,
                    "efficiency": round(efficiency - (index * 0.35), 1),
                    "voltage": round(base_voltage + math.sin(index + current_hour) * 1.6, 1),
                    "current": round(base_current * modulation, 1),
                    "power": power,
                    "temperature": round(base_temp + math.cos(index + current_hour) * 1.8, 1),
                    "surface_area": round(10.5 + index * 1.3, 1),
                }
            )
        return panels

    def _build_batteries(self) -> list[dict]:
        charge_wave = (math.sin(datetime.now().minute / 8) + 1) / 2
        return [
            {
                "id": "BAT-01",
                "name": "Banco de Litio Principal",
                "chemistry": "Lithium",
                "charge": round(72 + charge_wave * 14, 1),
                "capacity_kwh": 18.0,
                "voltage": 51.4,
                "cycles": 248,
                "status": "Cargando",
            },
            {
                "id": "BAT-02",
                "name": "Respaldo de Acido-Plomo",
                "chemistry": "Lead Acid",
                "charge": round(48 + charge_wave * 10, 1),
                "capacity_kwh": 12.0,
                "voltage": 47.8,
                "cycles": 413,
                "status": "Descargando",
            },
        ]

    def _build_loads(self) -> list[dict]:
        return [
            {
                "id": "LD-01",
                "name": "Iluminacion perimetral",
                "priority": "Alta",
                "consumption_w": 820,
                "source": "Solar",
                "status": "Activa",
            },
            {
                "id": "LD-02",
                "name": "Bomba de riego",
                "priority": "Media",
                "consumption_w": 1460,
                "source": "Bateria",
                "status": "Activa",
            },
            {
                "id": "LD-03",
                "name": "Centro de monitoreo",
                "priority": "Critica",
                "consumption_w": 620,
                "source": "Hibrida",
                "status": "Protegida",
            },
            {
                "id": "LD-04",
                "name": "Carga de vehiculos livianos",
                "priority": "Baja",
                "consumption_w": 2180,
                "source": "Solar",
                "status": "Programada",
            },
        ]

    def _build_alerts(self) -> list[dict]:
        now = datetime.now()
        return [
            {
                "id": "AL-104",
                "severity": "Critica",
                "message": "El panel PV-04 necesita revision por caida sostenida de eficiencia.",
                "time": (now - timedelta(minutes=7)).strftime("%H:%M"),
                "category": "Paneles",
            },
            {
                "id": "AL-103",
                "severity": "Media",
                "message": "La bateria BAT-02 cambio a modo de descarga para cubrir la bomba de riego.",
                "time": (now - timedelta(minutes=19)).strftime("%H:%M"),
                "category": "Baterias",
            },
            {
                "id": "AL-102",
                "severity": "Informativa",
                "message": "La produccion solar se recupero despues del paso de nubosidad parcial.",
                "time": (now - timedelta(minutes=31)).strftime("%H:%M"),
                "category": "Generacion",
            },
            {
                "id": "AL-101",
                "severity": "Media",
                "message": "Se reprogramo la carga de vehiculos para priorizar almacenamiento.",
                "time": (now - timedelta(minutes=46)).strftime("%H:%M"),
                "category": "Cargas",
            },
        ]

    def _build_hourly_generation(self) -> list[dict]:
        bars: list[dict] = []
        for hour in range(6, 19):
            intensity = max(0.12, math.sin(((hour - 6) / 12) * math.pi))
            bars.append(
                {
                    "label": f"{hour:02d}:00",
                    "value": round(1.4 + intensity * 6.2, 1),
                }
            )
        return bars

    async def get_dashboard_payload(self) -> dict:
        panels = self._build_panels()
        batteries = self._build_batteries()
        loads = self._build_loads()
        alerts = self._build_alerts()
        hourly_generation = self._build_hourly_generation()

        total_power = round(sum(panel["power"] for panel in panels), 2)
        avg_temperature = round(
            sum(panel["temperature"] for panel in panels) / len(panels), 1
        )
        battery_charge = round(
            sum(battery["charge"] for battery in batteries) / len(batteries), 1
        )
        active_loads = sum(1 for load in loads if load["status"] in {"Activa", "Protegida"})

        return {
            "summary": {
                "total_power_kw": total_power,
                "solar_generation_kw": round(total_power * 0.93, 2),
                "battery_level_pct": battery_charge,
                "avg_temperature_c": avg_temperature,
                "daily_savings_usd": round(total_power * 4.6, 2),
                "active_loads": active_loads,
            },
            "panels": panels,
            "batteries": batteries,
            "loads": loads,
            "alerts": alerts[:3],
            "hourly_generation": hourly_generation,
            "updated_at": datetime.now().strftime("%H:%M:%S"),
        }

    async def get_panels_payload(self) -> dict:
        panels = self._build_panels()
        return {
            "panels": panels,
            "totals": {
                "installed_capacity_kw": round(sum(panel["power"] for panel in panels) * 1.24, 2),
                "avg_efficiency": round(
                    sum(panel["efficiency"] for panel in panels) / len(panels), 1
                ),
                "active_panels": sum(1 for panel in panels if panel["status"] == "Activo"),
            },
            "updated_at": datetime.now().strftime("%H:%M:%S"),
        }

    async def get_batteries_payload(self) -> dict:
        batteries = self._build_batteries()
        available_storage = sum(
            battery["capacity_kwh"] * (battery["charge"] / 100) for battery in batteries
        )
        return {
            "batteries": batteries,
            "totals": {
                "available_storage_kwh": round(available_storage, 2),
                "bank_health_pct": 91.4,
                "autonomy_hours": round(available_storage / 2.9, 1),
            },
            "updated_at": datetime.now().strftime("%H:%M:%S"),
        }

    async def get_loads_payload(self) -> dict:
        loads = self._build_loads()
        return {
            "loads": loads,
            "totals": {
                "consumption_kw": round(sum(load["consumption_w"] for load in loads) / 1000, 2),
                "critical_loads": sum(1 for load in loads if load["priority"] == "Critica"),
                "scheduled_loads": sum(1 for load in loads if load["status"] == "Programada"),
            },
            "updated_at": datetime.now().strftime("%H:%M:%S"),
        }

    async def get_alerts_payload(self) -> dict:
        alerts = self._build_alerts()
        return {
            "alerts": alerts,
            "totals": {
                "critical": sum(1 for alert in alerts if alert["severity"] == "Critica"),
                "medium": sum(1 for alert in alerts if alert["severity"] == "Media"),
                "informative": sum(
                    1 for alert in alerts if alert["severity"] == "Informativa"
                ),
            },
            "updated_at": datetime.now().strftime("%H:%M:%S"),
        }


energy_service = EnergyService()
