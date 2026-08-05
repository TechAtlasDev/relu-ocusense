from datetime import datetime, timedelta
from langchain_core.tools import tool


@tool
def programar_seguimiento_cita(
    fecha_proxima_cita: str,
    especialidad: str,
    frecuencia_terapia_semanal: int = 2,
) -> dict:
    """Programa la continuidad terapéutica y el seguimiento de citas para reducir inasistencias.

    Args:
        fecha_proxima_cita: Fecha programada en formato YYYY-MM-DD.
        especialidad: Especialidad o tipo de terapia (ej. 'Terapia de Lenguaje', 'Neuropediatría').
        frecuencia_terapia_semanal: Cantidad de sesiones semanales recomendadas.

    Returns:
        Diccionario con la agenda de seguimiento y recomendaciones de adherencia.
    """
    try:
        fecha_dt = datetime.strptime(fecha_proxima_cita, "%Y-%m-%d")
        recordatorio_1 = (fecha_dt - timedelta(days=3)).strftime("%Y-%m-%d")
        recordatorio_2 = (fecha_dt - timedelta(days=1)).strftime("%Y-%m-%d")
    except ValueError:
        recordatorio_1 = "3 días antes de la cita"
        recordatorio_2 = "1 día antes de la cita"

    return {
        "especialidad": especialidad,
        "fecha_cita": fecha_proxima_cita,
        "frecuencia_semanal_recomendada": frecuencia_terapia_semanal,
        "recordatorios_programados": [
            f"Recordatorio inicial: {recordatorio_1}",
            f"Recordatorio final y verificación de pasajes/traslado: {recordatorio_2}",
        ],
        "estrategias_adherencia": [
            "Confirmar disponibilidad de transporte o apoyo familiar con 48 horas de anticipación.",
            "Llevar el resumen multidisciplinario de historia clínica a la cita.",
            "En caso de imprevisto, reprogramar la cita inmediatamente vía sistema o bot.",
        ],
    }


@tool
def obtener_plan_refuerzo_hogar(condicion_suspecta: str, edad_meses: int) -> dict:
    """Obtiene un conjunto de actividades prácticas de refuerzo para realizar en casa mientras se espera la atención especializada.

    Args:
        condicion_suspecta: Condición sospechada ('TEA', 'TDAH', 'Retraso_Lenguaje', 'Retraso_Motor').
        edad_meses: Edad en meses del paciente.

    Returns:
        Diccionario con pautas y ejercicios estructurados para cuidadores y docentes.
    """
    cond = condicion_suspecta.upper()

    if "TEA" in cond:
        actividades = [
            "Establecer rutinas diarias visuales estructuradas (pictogramas o imágenes de actividades).",
            "Juegos cara a cara con contacto visual libre de presión (juegos de escondite de rostro).",
            "Anticipar verbalmente cualquier cambio en la rutina con minutos de antelación.",
            "Crear un espacio tranquilo en casa para autorregulación sensorial cuando exista sobreestimulación.",
        ]
    elif "TDAH" in cond:
        actividades = [
            "Dividir las tareas o instrucciones en pasos únicos y sencillos.",
            "Establecer periodos breves de juego focalizado (10-15 minutos) alternados con movimiento libre.",
            "Refuerzo positivo inmediato ante conductas de atención logradas.",
            "Limitar pantallas e hiperestimulación digital antes de dormir.",
        ]
    elif "LENGUAJE" in cond:
        actividades = [
            "Leer cuentos ilustrados diariamente respondiendo a los señalamientos del niño.",
            "Cantar canciones sencillas con gestos y pausas deliberadas para dar tiempo a que responda.",
            "Nombrar en voz alta los objetos del entorno cotidiano sin presionar la pronunciación perfecta.",
            "Evitar adivinar las necesidades del niño antes de que intente comunicarse vocalmente o con gestos.",
        ]
    else:
        actividades = [
            "Ejercicios de juego en suelo con texturas diversas y pelotas suaves.",
            "Fomentar la exploración motora segura con supervisión.",
            "Mantener interacciones conversacionales continuas durante las comidas y el baño.",
        ]

    return {
        "condicion_suspecta": condicion_suspecta,
        "edad_meses": edad_meses,
        "dirigido_a": "Padres, cuidadores y educadores",
        "actividades_recomendadas": actividades,
        "nota_importante": "Estas pautas complementan y no sustituyen el tratamiento terapéutico profesional.",
    }
