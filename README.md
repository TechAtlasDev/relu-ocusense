# ⚡ ReLU - Cardio Alerta Perú (INSN-SB)

<p align="center">
  <img src="https://res.cloudinary.com/de1xmnmeq/image/upload/v1785792488/Slide_4_3_-_1_1_p8daej.png" alt="Cardio Alerta Perú Banner" width="100%" />
</p>

<p align="center">
  <img src="https://res.cloudinary.com/de1xmnmeq/image/upload/v1785792487/Slide_4_3_-_2_tk4vut.png" alt="ReLU Bot Logo" width="140" />
</p>

Repositorio oficial del proyecto **ReLU ⚡🤖**, un copiloto clínico asíncrono y asistente de tele-referencia desarrollado para la identificación oportuna de Cardiopatías Congénitas Críticas (CCC) en recién nacidos, adaptado a la altitud (m.s.n.m.) y a las realidades del primer nivel de atención en el Perú en colaboración con el **Instituto Nacional de Salud del Niño San Borja (INSN-SB)**.

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

- 🫀 **[Fase 1: Rol Clínico y Detección de Síntomas](backend/docs/cardio_alerta_fase1.md)**: Detalle del comportamiento de ReLU para personal médico SERUMS y orientación empática a familias (detección de síntomas invisibles).
- ⛰️ **[Fase 2: Herramienta de Tamizaje Ajustada por Altitud](backend/docs/cardio_alerta_fase2.md)**: Algoritmo ReAct en `@tool` para oximetría pre/post-ductal adaptada a metros sobre el nivel del mar (m.s.n.m.).
- 🚨 **[Fase 3: Alertas de Interconsulta e Integración SIS/FUA](backend/docs/cardio_alerta_fase3.md)**: Herramientas `@tool` para generar tickets de interconsulta hacia el INSN-SB y borradores automáticos de fichas SIS/FUA.
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
