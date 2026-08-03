# ⚡ ReLU - Backend Bot Telegram (Cardio Alerta Perú - INSN-SB)

<p align="center">
  <img src="https://res.cloudinary.com/de1xmnmeq/image/upload/v1785792488/Slide_4_3_-_1_1_p8daej.png" alt="Cardio Alerta Perú Banner" width="100%" />
</p>

<p align="center">
  <img src="https://res.cloudinary.com/de1xmnmeq/image/upload/v1785792487/Slide_4_3_-_2_tk4vut.png" alt="ReLU Bot Logo" width="140" />
</p>

Backend del bot de Telegram **ReLU ⚡🤖**, un copiloto clínico asíncrono y asistente de tele-referencia desarrollado para el tamizaje oportuno de Cardiopatías Congénitas Críticas (CCC) en recién nacidos, adaptado a la altitud y realidades del primer nivel de atención en el Perú en alianza estratégica con el **INSN-San Borja**.

---

## 👥 Equipo Desarrollador

<p align="center">
  <a href="https://ocusense.tech/" target="_blank">
    <img src="https://res.cloudinary.com/de1xmnmeq/image/upload/v1785792487/Slide_4_3_-_3_lgbctz.png" alt="OcuSense Team" width="100%" />
  </a>
</p>

Desarrollado con pasión por el equipo de **[OcuSense](https://ocusense.tech/)**. Visita nuestra web oficial en **[ocusense.tech](https://ocusense.tech/)**.

---

## 🚀 Inicio Rápido

### Prerrequisitos
- Python `>= 3.12`
- Administrador de paquetes [`uv`](https://github.com/astral-sh/uv)

### Instalación y Ejecución

1. Configura tus variables de entorno en el archivo `.env`:
   ```bash
   cp .env.example .env
   ```
   *Agrega tu `TELEGRAM_BOT_TOKEN` y `GEMINI_API_KEY`.*

2. Ejecuta el servidor del bot:
   ```bash
   uv run main.py
   ```

3. Ejecuta las pruebas automatizadas:
   ```bash
   uv run pytest
   ```

---

## 📚 Documentación del Proyecto

El repositorio cuenta con documentación detallada sobre su arquitectura, pruebas y guías de desarrollo:

- 🫀 **[Fase 1: Rol Clínico y Detección de Síntomas](file:///home/techatlasdev/Proyectos/OculusLab/hackaton/backend/docs/cardio_alerta_fase1.md)**: Detalle del comportamiento de ReLU para personal médico SERUMS y orientación empática a familias (detección de síntomas invisibles).
- ⛰️ **[Fase 2: Herramienta de Tamizaje Ajustada por Altitud](file:///home/techatlasdev/Proyectos/OculusLab/hackaton/backend/docs/cardio_alerta_fase2.md)**: Algoritmo ReAct en `@tool` para oximetría pre/post-ductal adaptada a metros sobre el nivel del mar (m.s.n.m.).
- 🚨 **[Fase 3: Alertas de Interconsulta e Integración SIS/FUA](file:///home/techatlasdev/Proyectos/OculusLab/hackaton/backend/docs/cardio_alerta_fase3.md)**: Herramientas `@tool` para generar tickets de interconsulta hacia el INSN-SB y borradores automáticos de fichas SIS/FUA.
- ☁️ **[Despliegue en Cloud Run & CI/CD](file:///home/techatlasdev/Proyectos/OculusLab/hackaton/backend/docs/cloud_run_cicd.md)**: Guía completa del Dockerfile, pipeline de GitHub Actions e inyección de secretos para Google Cloud Run.
- ⚡ **[Arquitectura LLM & Guía de Pruebas](file:///home/techatlasdev/.gemini/antigravity-ide/brain/022df3af-a9a7-4a55-8a03-c57fd43850cd/llm_architecture_and_testing.md)**: Documentación completa del flujo en LangGraph, streaming, suite de pruebas y guía para expandir herramientas.
- 🗺️ **[Roadmap del Desafío Cardio Alerta Perú](file:///home/techatlasdev/.gemini/antigravity-ide/brain/022df3af-a9a7-4a55-8a03-c57fd43850cd/roadmap_cardio_alerta.md)**: Plan estratégico de implementación para la hackatón.

---

## 🏗️ Estructura del Código

```
backend/
├── app/
│   ├── config.py         # Configuración con pydantic-settings
│   ├── handlers/         # Manejadores de eventos de Telegram Bot API
│   ├── services/
│   │   ├── agent.py      # Grafo de estados LangGraph y System Prompt de ReLU
│   │   └── llm.py        # Servicio de streaming LLM asíncrono
│   ├── tools/            # Herramientas ReAct (Tamizaje, Referencia SIS, etc.)
│   └── utils/            # Formateador sanitizado de Markdown
├── docs/                 # Documentación técnica del proyecto
├── tests/                # Suite de pruebas unitarias con pytest
├── Dockerfile            # Contenedor optimizado para Cloud Run
├── main.py               # Punto de entrada principal
└── pyproject.toml        # Configuración de dependencias con uv
```
