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
            const fill = document.getElementById('battery-fill');
            if (fill) fill.style.width = `${data.battery_lvl}%`;
        }
        if (cons) cons.innerText = `${data.energy_cons} kW`;

        // Actualizar gráfica si existe
        if (data.chart_data && document.getElementById('energyChart')) {
            this.updateChart(data.chart_data);
        }
    }

    updateChart(chartData) {
        if (!this.chart) {
            const ctx = document.getElementById('energyChart').getContext('2d');
            this.chart = new Chart(ctx, {
                type: chartData.tipo || 'line',
                data: {
                    labels: chartData.etiquetas,
                    datasets: [
                        {
                            label: chartData.titulo || 'Producción (kW)',
                            data: chartData.valores,
                            borderColor: '#4CAF50',
                            backgroundColor: 'rgba(76, 175, 80, 0.1)',
                            fill: true,
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { 
                            display: true, 
                            labels: { color: '#A0A0A0', font: { family: 'Outfit' } } 
                        } 
                    },
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#A0A0A0' } },
                        x: { grid: { display: false }, ticks: { color: '#A0A0A0' } }
                    }
                }
            });
        } else {
            this.chart.data.labels = chartData.etiquetas;
            this.chart.data.datasets[0].data = chartData.valores;
            if (chartData.titulo) this.chart.data.datasets[0].label = chartData.titulo;
            this.chart.update();
        }
    }
}

document.addEventListener('DOMContentLoaded', () => new EcoVoltApp());
