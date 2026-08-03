# 🛠️ Backend Técnico - ReLU Bot (Cardio Alerta Perú)

Documentación técnica y arquitectura de código para el backend del bot de Telegram **ReLU ⚡🤖**.

---

## 📌 Arquitectura del Backend

El backend está construido en **Python 3.12+** utilizando una arquitectura orientada a grafos con **LangGraph** y la API de **Google Gemini** (`gemini-2.5-flash`), integrada asíncronamente con la **Telegram Bot API**.

```mermaid
graph TD
    Telegram[📱 Telegram Bot API] <--> Handlers[📥 app/handlers/general.py]
    Handlers <--> LLMService[⚡ app/services/llm.py: Streaming]
    LLMService <--> LangGraph[🧠 app/services/agent.py: StateGraph ReAct]
    LangGraph <--> Tools[⚙️ app/tools/: Tamizaje / Referencia SIS / Calculadora]
```

---

## ⚙️ Componentes Clave del Código

| Directorio / Archivo | Función Principal |
| :--- | :--- |
| **`main.py`** | Punto de entrada del bot. Inicializa `ApplicationBuilder` de Telegram con el token configurado. |
| **`app/config.py`** | Gestión de configuración y secretos mediante `pydantic-settings`. |
| **`app/services/agent.py`** | Grafo `StateGraph` de LangGraph, memoria persistente por usuario (`MemorySaver`) y definición del `RELU_SYSTEM_PROMPT`. |
| **`app/services/llm.py`** | Servicio que invoca el grafo en modo streaming (`astream`) y emite las deltas y eventos de uso de herramientas. |
| **`app/handlers/general.py`** | Manejador de eventos de Telegram. Administra las ediciones dinámicas de streaming y el envío independiente de notificaciones de herramientas. |
| **`app/tools/tamizaje.py`** | Herramienta `@tool` `evaluar_tamizaje_oximetria` para cálculo de saturación ajustada por altitud m.s.n.m. |
| **`app/tools/referencia.py`** | Herramientas `@tool` `emitir_alerta_teleinterconsulta_insn` y `generar_ficha_referencia_sis`. |
| **`app/utils/formatter.py`** | Formateador y balanceador de sintaxis Markdown para evitar errores de renderizado en la API de Telegram. |

---

## 🧪 Pruebas Automatizadas

El backend incluye una suite completa de unit tests con `pytest` y `pytest-asyncio`.

```bash
# Ejecutar todas las pruebas
uv run pytest

# Ejecutar un módulo específico
uv run pytest tests/test_tamizaje.py -v
```

---

## 🐳 Contenedor Docker para Cloud Run

El archivo `Dockerfile` en este directorio compila una imagen ligera basada en `python:3.12-slim` e instala las dependencias en el sistema con `uv pip install --system`.

- **Puerto Expuesto:** `8080` (configurado mediante la variable `PORT`).
- **Comando de Ejecución:** `python main.py`.
