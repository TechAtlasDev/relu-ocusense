# ReLU - Neuroalianza: Ruta Multidisciplinaria para Salud, Familia y Neurodesarrollo

Repositorio oficial del proyecto **ReLU**, un copiloto clínico asíncrono y asistente de tele-referencia desarrollado para la detección temprana, derivación oportuna y seguimiento continuo de trastornos del neurodesarrollo infantojuvenil (TEA, TDAH, retrasos del desarrollo y lenguaje) en el Perú.

---

## Inicio Rápido

### Prerrequisitos
- Python `>= 3.12`
- Administrador de paquetes [`uv`](https://github.com/astral-sh/uv)

### Instalación y Ejecución del Backend

1. Entra al directorio del backend y configura las variables de entorno:
   ```bash
   cd backend
   cp .env.example .env
   ```
   *Configura `TELEGRAM_BOT_TOKEN` y `GEMINI_API_KEY`.*

2. Ejecuta el servidor del bot:
   ```bash
   uv run main.py
   ```

3. Ejecuta la suite de pruebas automatizadas:
   ```bash
   uv run pytest
   ```

---

## Documentación del Proyecto

- **[Fase 1: Rol Clínico, Detección Inicial y Acompañamiento Familiar](backend/docs/neuroalianza_fase1.md)**: Guía de interacción para personal CRED/SERUMS y orientación a cuidadores.
- **[Fase 2: Herramienta de Tamizaje y Evaluación de Riesgo](backend/docs/neuroalianza_fase2.md)**: Algoritmo ReAct en `@tool` para evaluación con M-CHAT-R/F, EEDP/TPED y Vanderbilt.
- **[Fase 3: Tele-referencia, FUA/SIS y Seguimiento Terapéutico](backend/docs/neuroalianza_fase3.md)**: Herramientas `@tool` para tickets de tele-interconsulta, FUA/SIS (CIE-10 F84, F90, F80) y planes de refuerzo.
- **[Despliegue en Cloud Run & CI/CD](backend/docs/cloud_run_cicd.md)**: Guía completa del Dockerfile, pipeline de GitHub Actions e inyección de secretos para Google Cloud Run.

---

## Estructura del Repositorio

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD Workflow para Google Cloud Run
├── backend/
│   ├── app/                # Código fuente del bot (handlers, services, tools)
│   ├── docs/               # Documentación técnica específica por fases
│   ├── tests/              # Pruebas automatizadas con pytest
│   ├── Dockerfile          # Contenedor optimizado para Cloud Run
│   ├── main.py             # Punto de entrada principal
│   └── pyproject.toml      # Gestión de dependencias con uv
└── README.md               # Documentación principal del repositorio
```

---

## Equipo Desarrollador

Desarrollado por el equipo de **OcuSense**. Visita nuestra web oficial en **[ocusense.tech](https://ocusense.tech/)**.
