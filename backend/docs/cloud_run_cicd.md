# ☁️ Guía de Despliegue en Google Cloud Run & CI/CD

Documentación para el despliegue automatizado del backend de **ReLU** en **Google Cloud Run** usando **GitHub Actions**.

---

## 🏗️ Estructura del Repositorio Raíz

El repositorio ha sido inicializado en la carpeta raíz del proyecto conteniendo el subdirectorio `backend/`:

```
/ (Raíz del Repositorio Git)
├── .github/
│   └── workflows/
│       └── deploy.yml          # Flujo de CI/CD para Cloud Run
├── backend/
│   ├── app/                    # Código del agente y herramientas
│   ├── docs/                   # Documentación de fases Cardio Alerta Perú
│   ├── tests/                  # Suite de pruebas con pytest
│   ├── Dockerfile              # Contenedor optimizado para Cloud Run (puerto 8080)
│   ├── main.py                 # Punto de entrada principal
│   └── pyproject.toml          # Gestión de dependencias con uv
└── .gitignore                  # Exclusiones de secretos (.env, .venv, etc.)
```

---

## 🐳 Dockerfile Optimizado

El archivo [backend/Dockerfile](file:///home/techatlasdev/Proyectos/OculusLab/hackaton/backend/Dockerfile) utiliza `python:3.12-slim` e instala `uv` para garantizar compilaciones ultrarrápidas y sin caché innecesaria. Expone el puerto `8080` requerido por Google Cloud Run.

---

## ⚡ Workflow de CI/CD (GitHub Actions)

Ubicado en [.github/workflows/deploy.yml](file:///home/techatlasdev/Proyectos/OculusLab/hackaton/.github/workflows/deploy.yml).

### Etapas del Pipeline:
1. **Testing:** Ejecuta la suite completa de pruebas asíncronas con `pytest` mediante `uv`.
2. **Autenticación GCP:** Se autentica de forma segura con Google Cloud usando una cuenta de servicio.
3. **Build & Push Docker:** Compila la imagen y la publica en **Google Artifact Registry**.
4. **Deploy a Cloud Run:** Despliega el contenedor expuesto e inyecta las variables de entorno de producción.

---

## 🔑 Secretos Requeridos en GitHub (Repository Secrets)

Para habilitar el flujo de despliegue automático al hacer push a `master`/`main`, agrega los siguientes secretos en **GitHub -> Settings -> Secrets and variables -> Actions**:

| Nombre del Secreto | Descripción |
| :--- | :--- |
| `GCP_PROJECT_ID` | ID de tu proyecto en Google Cloud Platform. |
| `GCP_SA_KEY` | Clave JSON de la cuenta de servicio de GCP con permisos para Artifact Registry y Cloud Run. |
| `GCP_REGION` | *(Opcional)* Región de GCP (ejemplo: `us-central1`). |
| `TELEGRAM_BOT_TOKEN` | Token oficial de tu bot de Telegram obtenido vía BotFather. |
| `GEMINI_API_KEY` | Clave de API de Google Gemini. |
