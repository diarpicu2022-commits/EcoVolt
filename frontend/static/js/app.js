const currentPage = document.body.dataset.page;
const updatedAtElement = document.getElementById("updated-at");

function setUpdatedAt(value) {
    if (updatedAtElement) {
        updatedAtElement.textContent = value;
    }
}

function updateSummaryFields(summary) {
    if (!summary) {
        return;
    }

    const summaryMap = {
        total_power_kw: Number(summary.total_power_kw).toFixed(2),
        solar_generation_kw: Number(summary.solar_generation_kw).toFixed(2),
        battery_level_pct: Number(summary.battery_level_pct).toFixed(1),
        avg_temperature_c: Number(summary.avg_temperature_c).toFixed(1),
        daily_savings_usd: Number(summary.daily_savings_usd).toFixed(2),
        active_loads: summary.active_loads,
    };

    Object.entries(summaryMap).forEach(([field, value]) => {
        const target = document.querySelector(`[data-field="${field}"]`);
        if (target) {
            target.textContent = value;
        }
    });
}

function updateTotalsFields(totals) {
    if (!totals) {
        return;
    }

    Object.entries(totals).forEach(([field, value]) => {
        const target = document.querySelector(`[data-field="${field}"]`);
        if (target) {
            target.textContent = typeof value === "number" ? value.toFixed(2).replace(/\.00$/, "") : value;
        }
    });
}

function renderDashboard(data) {
    updateSummaryFields(data.summary);
    setUpdatedAt(data.updated_at);

    const generationElement = document.getElementById("hourly-generation");
    if (generationElement) {
        generationElement.innerHTML = data.hourly_generation.map((item) => `
            <div class="bar-item">
                <div class="bar-track">
                    <div class="bar-fill" style="height: ${(item.value / 8) * 100}%"></div>
                </div>
                <strong>${item.value}</strong>
                <span>${item.label}</span>
            </div>
        `).join("");
    }

    const panelsElement = document.getElementById("dashboard-panels");
    if (panelsElement) {
        panelsElement.innerHTML = data.panels.slice(0, 3).map((panel) => `
            <div class="list-row">
                <div>
                    <strong>${panel.name}</strong>
                    <span>${panel.id} · ${panel.status}</span>
                </div>
                <b>${panel.power} kW</b>
            </div>
        `).join("");
    }

    const loadsElement = document.getElementById("dashboard-loads");
    if (loadsElement) {
        loadsElement.innerHTML = data.loads.slice(0, 3).map((load) => `
            <div class="list-row">
                <div>
                    <strong>${load.name}</strong>
                    <span>${load.priority} · ${load.source}</span>
                </div>
                <b>${load.consumption_w} W</b>
            </div>
        `).join("");
    }

    const alertsElement = document.getElementById("dashboard-alerts");
    if (alertsElement) {
        alertsElement.innerHTML = data.alerts.map((alert) => `
            <div class="alert-row severity-${normalizeSeverity(alert.severity)}">
                <div>
                    <strong>${alert.category}</strong>
                    <p>${alert.message}</p>
                </div>
                <span>${alert.time}</span>
            </div>
        `).join("");
    }
}

function renderPanels(data) {
    updateTotalsFields(data.totals);
    setUpdatedAt(data.updated_at);

    const tableBody = document.getElementById("panels-table");
    if (tableBody) {
        tableBody.innerHTML = data.panels.map((panel) => `
            <tr>
                <td>${panel.id}</td>
                <td>${panel.name}</td>
                <td><span class="status-pill">${panel.status}</span></td>
                <td>${panel.efficiency}%</td>
                <td>${panel.voltage} V</td>
                <td>${panel.current} A</td>
                <td>${panel.power} kW</td>
                <td>${panel.temperature} C</td>
            </tr>
        `).join("");
    }
}

function renderBatteries(data) {
    updateTotalsFields(data.totals);
    setUpdatedAt(data.updated_at);

    const cards = document.getElementById("battery-cards");
    if (cards) {
        cards.innerHTML = data.batteries.map((battery) => `
            <article class="panel-card battery-card">
                <div class="section-heading">
                    <div>
                        <p class="eyebrow">${battery.id}</p>
                        <h3>${battery.name}</h3>
                    </div>
                    <span class="status-pill">${battery.status}</span>
                </div>
                <div class="meter">
                    <div class="meter-fill" style="width: ${battery.charge}%"></div>
                </div>
                <div class="details-grid">
                    <div><span>Carga</span><strong>${battery.charge}%</strong></div>
                    <div><span>Capacidad</span><strong>${battery.capacity_kwh} kWh</strong></div>
                    <div><span>Voltaje</span><strong>${battery.voltage} V</strong></div>
                    <div><span>Ciclos</span><strong>${battery.cycles}</strong></div>
                </div>
            </article>
        `).join("");
    }
}

function renderLoads(data) {
    updateTotalsFields(data.totals);
    setUpdatedAt(data.updated_at);

    const list = document.getElementById("loads-list");
    if (list) {
        list.innerHTML = data.loads.map((load) => `
            <div class="load-card">
                <div>
                    <strong>${load.name}</strong>
                    <span>${load.id} · ${load.priority} · ${load.source}</span>
                </div>
                <div class="load-meta">
                    <b>${load.consumption_w} W</b>
                    <span class="status-pill">${load.status}</span>
                </div>
            </div>
        `).join("");
    }
}

function renderAlerts(data) {
    updateTotalsFields(data.totals);
    setUpdatedAt(data.updated_at);

    const list = document.getElementById("alerts-list");
    if (list) {
        list.innerHTML = data.alerts.map((alert) => `
            <div class="alert-row severity-${normalizeSeverity(alert.severity)}">
                <div>
                    <strong>${alert.category} · ${alert.severity}</strong>
                    <p>${alert.message}</p>
                </div>
                <span>${alert.time}</span>
            </div>
        `).join("");
    }
}

function normalizeSeverity(value) {
    return value.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

async function refreshCurrentPage() {
    const endpointMap = {
        dashboard: "/api/dashboard",
        paneles: "/api/panels",
        baterias: "/api/batteries",
        cargas: "/api/loads",
        alertas: "/api/alerts",
    };

    const rendererMap = {
        dashboard: renderDashboard,
        paneles: renderPanels,
        baterias: renderBatteries,
        cargas: renderLoads,
        alertas: renderAlerts,
    };

    const endpoint = endpointMap[currentPage];
    const renderer = rendererMap[currentPage];

    if (!endpoint || !renderer) {
        return;
    }

    try {
        const response = await fetch(endpoint, { headers: { "Cache-Control": "no-store" } });
        if (!response.ok) {
            return;
        }
        const data = await response.json();
        renderer(data);
    } catch (error) {
        console.warn("EcoVolt refresh skipped", error);
    }
}

refreshCurrentPage();
window.setInterval(refreshCurrentPage, 5000);
