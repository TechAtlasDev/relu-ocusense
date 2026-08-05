# ⚡ ReLU - Neuroalianza Perú (INSN-SB)

<p align="center">
  <img src="https://res.cloudinary.com/de1xmnmeq/image/upload/v1785792488/Slide_4_3_-_1_1_p8daej.png" alt="Neuroalianza Perú Banner" width="100%" />
</p>

Repositorio oficial del proyecto **ReLU ⚡🤖**, un copiloto clínico asíncrono y asistente de tele-referencia desarrollado para la detección temprana, derivación oportuna y seguimiento continuo de **Trastornos del Neurodesarrollo (TEA, TDAH, retrasos del desarrollo psicomotor y del lenguaje)** en recién nacidos, niños y adolescentes en el Perú, en colaboración con el **Instituto Nacional de Salud del Niño San Borja (INSN-SB)** y el primer nivel de atención.

---

## 🚀 Inicio Rápido

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

## 📚 Documentación del Proyecto

- 🧠 **[Fase 1: Rol Clínico, Detección Inicial y Acompañamiento Familiar](backend/docs/neuroalianza_fase1.md)**: Detalle del comportamiento de ReLU para personal CRED/SERUMS y orientación empática a familias (detección de señales de alerta tempranas).
- ⛰️ **[Fase 2: Herramientas de Tamizaje de Neurodesarrollo](backend/docs/neuroalianza_fase2.md)**: Algoritmo ReAct en `@tool` para evaluación con escalas estandarizadas (M-CHAT-R/F, EEDP/TPED, Vanderbilt).
- 🚨 **[Fase 3: Tele-referencia Multidisciplinaria, FUA/SIS y Seguimiento](backend/docs/neuroalianza_fase3.md)**: Herramientas `@tool` para generar tickets de interconsulta hacia neuropediatría/psicología, borradores de fichas SIS/FUA (CIE-10 F84, F90, F80) y planes de refuerzo en casa.
- ☁️ **[Despliegue en Cloud Run & CI/CD](backend/docs/cloud_run_cicd.md)**: Guía completa del Dockerfile, pipeline de GitHub Actions e inyección de secretos para Google Cloud Run.

---

## 🏗️ Estructura del Repositorio

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

## 👥 Equipo Desarrollador

<p align="center">
  <a href="https://ocusense.tech/" target="_blank">
    <img src="https://res.cloudinary.com/de1xmnmeq/image/upload/v1785792487/Slide_4_3_-_3_lgbctz.png" alt="OcuSense Team" width="100%" />
  </a>
</p>

Desarrollado con pasión por el equipo de **[OcuSense](https://ocusense.tech/)**. Visita nuestra web oficial en **[ocusense.tech](https://ocusense.tech/)**.
