# Fase 3: Tele-referencia Multidisciplinaria, FUA/SIS y Seguimiento Terapéutico

## 1. Visión General

La **Fase 3** abarca la conexión del paciente detectado con la red de atención especializada, la facilitación de trámites administrativos (FUA/SIS) y la estrategia continua para reducir las inasistencias a terapias y controles.

---

## 2. Emisión de Tele-referencias Multidisciplinarias

Herramienta: `emitir_referencia_neurodesarrollo`

Permite al personal de salud generar un ticket estructurado de derivación a institutos o centros de referencia (ej. INSN San Borja, INSN Breña, Hospitales Regionales):

- **Campos del Ticket:**
  - Código único de referencia.
  - Nombre del paciente y edad en meses.
  - Nivel de riesgo (Bajo / Moderado / Alto).
  - Especialidad solicitada (Neuropediatría, Psiquiatría Infantil, Psicología, Terapia de Lenguaje, Terapia Ocupacional).
  - Establecimiento de origen.
  - Resumen clínico inicial.

---

## 3. Integración de Borrador de Ficha FUA / SIS

Herramienta: `generar_ficha_fua_neurodesarrollo`

Prepara la información administrativa para la codificación en el Sistema de Formato Único de Atención (FUA/SIS) peruano:

### Códigos CIE-10 Frecuentes en Neurodesarrollo
- **F84.0:** Autismo infantil
- **F84.9:** Trastorno generalizado del desarrollo no especificado
- **F90.0:** Trastorno por déficit de atención e hiperactividad (TDAH), tipo combinado
- **F80.1:** Trastorno del lenguaje expresivo
- **F80.2:** Trastorno de la recepción del lenguaje
- **F82:** Trastorno específico del desarrollo de la función motora
- **R62.0:** Retraso del desarrollo psicomotor

---

## 4. Trazabilidad, Adherencia y Seguimiento Terapéutico

Herramientas: `programar_seguimiento_cita` y `obtener_plan_refuerzo_hogar`

### Factores de Inasistencia en el Perú
- Dificultades económicas y traslados geográficos extensos.
- Falta de claridad en la fecha y lugar de la cita.
- Sensación de falta de avance o desacoplamiento familiar.

### Estrategias de Adherencia en Neuroalianza
1. **Cronograma Terapéutico Claro:** Genera resúmenes de frecuencia semanal de terapias recomendadas.
2. **Pautas de Refuerzo en Casa:** Brinda a los cuidadores ejercicios diarios sencillos (ej. juegos de contacto visual, estructuración de rutinas visuales, estrategias de regulación sensorial) para realizar mientras se espera la cita especializada.
3. **Resumen Multidisciplinario:** Consolidado de la información del paciente para consulta ágil por parte del equipo médico.
