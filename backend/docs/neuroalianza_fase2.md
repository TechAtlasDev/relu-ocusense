# Fase 2: Herramienta de Tamizaje y Evaluación de Riesgo en Neurodesarrollo

## 1. Visión General

La **Fase 2** de **Neuroalianza** define la lógica de tamizaje estandarizado que ejecuta el agente ReAct a través de herramientas `@tool`. Permite evaluar el nivel de riesgo en neurodesarrollo basándose en escalas internacionales adaptadas al entorno peruano.

---

## 2. Escalas e Instrumentos Integrados

### A. Escala EEDP / TPED (Evaluación del Desarrollo CRED)
- **Población:** 0 a 30 meses.
- **Áreas Evaluadas:** Motora, Lenguaje, Social, Coordinación.
- **Resultado:** Desarrollo Normal, Riesgo de Retraso, Retraso Confirmado.

### B. M-CHAT-R/F (Modified Checklist for Autism in Toddlers)
- **Población:** 16 a 30 meses.
- **Enfoque:** Detección precoz de Trastornos del Espectro Autista (TEA).
- **Puntuación de Riesgo:**
  - **Riesgo Bajo (0-2 puntos):** Seguimiento en controles CRED habituales.
  - **Riesgo Moderado (3-7 puntos):** Re-evaluación con M-CHAT-R/F de seguimiento o derivación a psicología/pediatría.
  - **Riesgo Alto (8-20 puntos):** Referencia prioritaria a neuropediatría o psiquiatría infantil.

### C. Criterios Vanderbilt / Conners (TDAH y Conducta)
- **Población:** 6 a 17 años.
- **Enfoque:** Evaluación de Inatención, Hiperactividad/Impulsividad y desempeño académico/social.
- **Resultado:** Indicadores de sospecha alta para TDAH.

---

## 3. Lógica del Algoritmo ReAct (`evaluar_desarrollo_infantil`)

El agente analiza la entrada del usuario (edad en meses o años, síntomas y rol) y ejecuta la herramienta `evaluar_desarrollo_infantil`.

### Diagrama de Flujo
```
[Mensaje de Usuario] -> [Agente LLM Gemini]
                            |
                     (Llama a Tool)
                            |
             evaluar_desarrollo_infantil()
                            |
           +----------------+----------------+
           |                                 |
  [0 a 30 meses]                    [3 a 17 años]
  M-CHAT-R/F + CRED                Vanderbilt / Conducta
           |                                 |
           +----------------+----------------+
                            |
                   Estratificación de Riesgo
               (Riesgo Bajo / Moderado / Alto)
                            |
               [Respuesta Estructurada al Bot]
```

---

## 4. Clasificación y Conducta Recomendada

1. **Riesgo Bajo:**
   - Indicaciones para la familia sobre estimulación en el hogar.
   - Programación de próximo control CRED.

2. **Riesgo Moderado:**
   - Orientación sobre pautas específicas de lenguaje e interacción.
   - Evaluación complementaria por psicología o medicina general.

3. **Riesgo Alto:**
   - Activación inmediata del flujo de tele-referencia a especialidad (Neuropediatría / Psiquiatría infantil).
   - Generación de borrador de Ficha FUA/SIS.
