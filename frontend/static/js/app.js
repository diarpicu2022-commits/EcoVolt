class EcoVoltApp {
    constructor() {
        this.pollInterval = 5000;
        this.init();
    }

    init() {
        this.startPolling();
    }

    startPolling() {
        this.fetchMetrics();
        setInterval(() => this.fetchMetrics(), this.pollInterval);
    }

    async fetchMetrics() {
        try {
            const response = await fetch('/api/v1/metrics');
            const data = await response.json();
            this.updateUI(data);
        } catch (error) {
            console.error("Error al obtener métricas:", error);
        }
    }

    updateUI(data) {
        const solar = document.getElementById('solar-gen');
        const battery = document.getElementById('battery-lvl');
        const cons = document.getElementById('energy-cons');

        if (solar) solar.innerText = `${data.solar_gen} kW`;
        if (battery) {
            battery.innerText = `${data.battery_lvl}%`;
            document.getElementById('battery-fill')?.style.setProperty('width', `${data.battery_lvl}%`);
        }
        if (cons) cons.innerText = `${data.energy_cons} kW`;
    }
}

document.addEventListener('DOMContentLoaded', () => new EcoVoltApp());
