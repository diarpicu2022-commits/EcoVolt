# EcoVolt — Sistema de Energía Solar Inteligente
## Documento de Diseño — 2026-05-14

---

## 1. Descripción General

EcoVolt es un sistema de gestión de energía solar inteligente que monitorea paneles solares, baterías, cargas de consumo y alertas en tiempo real. Combina electrónica (sensores reales vía puerto serial) con software (simulación Python), presentando todo en un dashboard web en español.

**Stack:** Python 3.11+ · FastAPI · SQLite · HTML/CSS/JS (Jinja2 templates)

**Arquitectura:** Hexagonal (Ports & Adapters) — el dominio no conoce la fuente de datos (simulador vs. hardware real).

---

## 2. Módulos del Sistema

| Módulo | Entidades | Responsabilidad |
|---|---|---|
| **Paneles Solares** | MonocrystallinePanel, PolycrystallinePanel, ThinFilmPanel | Lectura de voltaje, corriente, potencia, eficiencia, temperatura |
| **Baterías** | LithiumBattery, LeadAcidBattery | Estado de carga, ciclos, voltaje, transiciones de estado |
| **Cargas/Consumo** | EnergyLoad | Dispositivos conectados, watts consumidos, prioridades |
| **Alertas** | EnergyAlert | Alertas por umbral: sobrecalentamiento, batería baja, fallo de panel |

---

## 3. Arquitectura Hexagonal

```
[Hardware Serial] ─┐
                   ├─► SensorAdapter ─► ISensorPort ─► DomainCore ─► ISQLitePort ─► SQLite
[Simulator Python] ─┘                                      │
                                                           └─► IAPIPort ─► FastAPI ─► HTML Templates
```

- El `DomainCore` nunca importa SQLite ni el puerto serial directamente.
- Los adaptadores implementan interfaces (puertos) definidas en el dominio.
- Cambiar de simulador a hardware real = cambiar 1 línea en `main.py`.

---

## 4. Estructuras de Datos — Implementación Completa

Todas implementadas desde cero en `backend/data_structures/`.

### 4.1 Arrays (`arrays/`)

| Archivo | Tipo | Uso en dominio solar |
|---|---|---|
| `solar_panel_static_array.py` | 1D estático (max 20) | Slots fijos de instalación |
| `solar_panel_dynamic_array.py` | 1D dinámico + QuickSort/MergeSort/HeapSort | Lista activa de paneles ordenados por eficiencia |
| `energy_production_matrix.py` | 2D `[panel][hora]` | kWh generado por panel por hora del día |
| `monthly_energy_volume.py` | 3D `[panel][día][mes]` | Producción histórica volumétrica |
| `sensor_polling_circular_array.py` | Circular (índice módulo) | Buffer circular de últimas N lecturas |
| `sensor_reading_struct_array.py` | Array de estructuras | Array de objetos `SensorReading` |
| `panel_reference_array.py` | Array de referencias | Punteros a paneles activos en memoria |
| `alert_message_string_array.py` | Array de strings | Mensajes de alerta del sistema |

**Operaciones requeridas en todos los arrays:** `get()`, `set()`, `insertAt()`, `append()`, `deleteAt()`, `deleteValue()`, `findIndex()`, `contains()`, `sortAscending()`, `sortDescending()`

**Algoritmos de ordenamiento** en `solar_panel_dynamic_array.py`: QuickSort, MergeSort, HeapSort.

### 4.2 Queues (`queues/`)

| Archivo | Uso |
|---|---|
| `alert_processing_queue.py` | Cola FIFO de alertas pendientes de procesar |
| `sensor_event_queue.py` | Cola FIFO de eventos de lectura entrantes |

Operaciones: `enqueue()`, `dequeue()`, `front()`, `rear()`, `isEmpty()`, `size()`

### 4.3 Linked Lists (`linked_lists/`)

| Archivo | Tipo | Uso |
|---|---|---|
| `sensor_reading_singly_list.py` | Lista simple | Cadena de lecturas de sensor (solo forward) |
| `reading_history_doubly_list.py` | Lista doble | Historial navegable de lecturas (prev/next) |
| `panel_monitor_circular_list.py` | Lista circular doble | Round-robin de monitoreo de paneles |

### 4.4 Stacks (`stacks/`)

| Archivo | Uso |
|---|---|
| `configuration_command_stack.py` | Pila LIFO: undo/redo de configuraciones del sistema |

Operaciones: `push()`, `pop()`, `peek()`, `isEmpty()`

---

## 5. Patrones de Diseño — Los 11 Patrones

### 5.1 Creacionales (`patterns/creational/`)

#### Singleton (3 instancias)
- `system_logger.py` — Logger global único del sistema
- `solar_system_config.py` — Configuración global única
- `database_connection.py` — Conexión SQLite única
- Estructura: constructor privado + `_instance` estático + `get_instance()`

#### Factory Method
- `sensor_reading_creator.py` — Creator abstracto con `factory_method()` abstracto
- `voltage_reading_creator.py` — Crea `VoltageReading`
- `temperature_reading_creator.py` — Crea `TemperatureReading`
- `current_reading_creator.py` — Crea `CurrentReading`

#### Abstract Factory
- `solar_panel_abstract_factory.py` — Interfaz de fábrica: `create_panel()`, `create_sensor()`, `create_controller()`
- `monocrystalline_factory.py` — Familia monocristalina
- `polycrystalline_factory.py` — Familia policristalina
- `thin_film_factory.py` — Familia thin film

#### Builder
- `energy_report_builder.py` — Construye `EnergyReport` paso a paso con secciones opcionales
- `energy_report_director.py` — Orquesta la construcción (reporte diario, semanal, mensual)

#### Prototype
- `panel_config_prototype.py` — `clone()` shallow/deep de configuraciones de panel

### 5.2 Estructurales (`patterns/structural/`)

#### Adapter
- `sensor_port.py` — Target (ISensorPort): `read_voltage()`, `read_current()`, `read_temperature()`
- `serial_hardware_adaptee.py` — Adaptee: API de puerto serial (incompatible)
- `serial_sensor_adapter.py` — Adapter para hardware real (Arduino/RPi)
- `simulator_sensor_adapter.py` — Adapter para datos simulados Python

#### Bridge
- `energy_display_abstraction.py` — Abstraction: `display(panel_id)`
- `panel_chart_display.py` — Refined abstraction: gráfica de panel
- `battery_chart_display.py` — Refined abstraction: gráfica de batería
- `chart_renderer.py` — Implementation interface: `render(data)`
- `json_chart_renderer.py` — ConcreteImpl: renderiza como JSON (para API REST)
- `html_chart_renderer.py` — ConcreteImpl: renderiza como HTML (para templates)

#### Decorator
- `sensor_data_decorator.py` — Decorator abstracto (wraps `ISensorPort`)
- `calibration_decorator.py` — Aplica factor de calibración a las lecturas
- `validation_decorator.py` — Valida rangos físicos (voltaje 0-50V, temp -10°C a 85°C)
- `noise_filter_decorator.py` — Filtra ruido eléctrico (moving average)

#### Facade
- `energy_management_facade.py` — API simplificada sobre paneles, baterías, cargas y alertas

#### Proxy
- `sensor_data_proxy.py` — Rate limiting (máx lecturas/seg) + logging + lazy loading del sensor

### 5.3 Comportamental (`patterns/behavioral/states/`)

#### State — Battery (4 estados)
- `battery_state.py` — State abstracto: `handle_charge()`, `handle_discharge()`, `get_status()`
- `charging_state.py` — Batería cargando
- `discharging_state.py` — Batería descargando
- `full_charge_state.py` — Batería llena
- `low_battery_state.py` — Batería baja (< 20%)

#### State — Panel (4 estados)
- `panel_state.py` — State abstracto: `handle_reading()`, `get_status()`
- `active_panel_state.py` — Panel generando energía normalmente
- `standby_panel_state.py` — Panel en espera (noche/nubes)
- `maintenance_panel_state.py` — Panel en mantenimiento
- `faulty_panel_state.py` — Panel con fallo detectado

**Regla:** Prohibido usar `if/else` o `switch` para transiciones de estado.

---

## 6. Jerarquía de Herencia (3 Niveles)

```
Nivel 1 (Abstract): EnergyComponent
    ├── Nivel 2 (Abstract): SolarPanel
    │       ├── Nivel 3 (Concrete): MonocrystallinePanel
    │       ├── Nivel 3 (Concrete): PolycrystallinePanel
    │       └── Nivel 3 (Concrete): ThinFilmPanel
    └── Nivel 2 (Abstract): Battery
            ├── Nivel 3 (Concrete): LithiumBattery
            └── Nivel 3 (Concrete): LeadAcidBattery
```

- `EnergyComponent`: campos `private`, métodos abstractos `generate()`, `get_status()`, `get_efficiency()`
- `SolarPanel`: agrega `panel_id`, `surface_area_m2`, `peak_power_watts`
- `Battery`: agrega `capacity_kwh`, `current_charge_percentage`, `cycle_count`

---

## 7. OOP — Reglas de Acceso

- Todos los campos: `private` (prefijo `__`) o `protected` (prefijo `_`)
- Getters/setters donde sea necesario
- Interfaces simuladas con clases ABC de Python (`abc.ABC`, `@abstractmethod`)
- Polimorfismo: overriding de `generate()`, `get_status()`, `get_efficiency()` en cada subclase

---

## 8. Reglas de Código

| Regla | Detalle |
|---|---|
| Identificadores | En inglés, contextuales al dominio solar |
| Comentarios | En español, explican el POR QUÉ |
| UI (labels, mensajes) | En español |
| Nombres genéricos | PROHIBIDOS: `data`, `item`, `temp`, `obj`, `value` |

---

## 9. Frontend

- **Framework:** FastAPI con Jinja2 templates
- **Páginas:** Dashboard, Paneles, Baterías, Cargas, Alertas
- **Estilo:** Tema solar (verde/amarillo/naranja), responsive
- **Actualización en tiempo real:** Polling JS cada 5s a endpoints REST
- **Idioma UI:** Español completo

---

## 10. Base de Datos

- **Motor:** SQLite (archivo único `ecovolt.db`)
- **Tablas:** `solar_panels`, `batteries`, `energy_loads`, `energy_alerts`, `sensor_readings`
- **Acceso:** Repository pattern vía interfaces (no acceso directo desde servicios)
- **Singleton:** `DatabaseConnection.get_instance()` maneja la conexión

---

## 11. Tests

Archivos en `backend/tests/`:
- `test_solar_panel.py` — herencia, polimorfismo, factory
- `test_battery_states.py` — transiciones de estado sin if/else
- `test_data_structures.py` — todas las estructuras de datos
- `test_patterns.py` — singleton, builder, prototype, decorator, proxy

---

## 12. Estructura de Carpetas Final

```
EcoVolt/
├── backend/
│   ├── main.py
│   ├── config/
│   ├── domain/
│   │   ├── entities/
│   │   └── interfaces/
│   ├── data_structures/
│   │   ├── arrays/
│   │   ├── queues/
│   │   ├── linked_lists/
│   │   └── stacks/
│   ├── patterns/
│   │   ├── creational/
│   │   ├── structural/
│   │   └── behavioral/states/
│   ├── services/
│   ├── repositories/
│   ├── api/routers/
│   ├── db/
│   └── tests/
└── frontend/
    ├── templates/
    └── static/
        ├── css/
        └── js/
```

---

*Documento generado: 2026-05-14 | Proyecto: EcoVolt — Tarea Final Estructura de Software*
