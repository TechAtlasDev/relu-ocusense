import uuid
from datetime import datetime
from langchain_core.tools import tool


@tool
def generar_resumen_caso_multidisciplinario(
    nombre_paciente: str,
    edad_meses: int,
    antecedentes_cred: str,
    evaluaciones_realizadas: list[str],
    nivel_riesgo_actual: str,
) -> dict:
    """Consolida el historial del paciente en un resumen multidisciplinario listo para ser revisado por el especialista.

    Args:
        nombre_paciente: Nombre o iniciales del paciente.
        edad_meses: Edad en meses.
        antecedentes_cred: Resumen de hallazgos del control CRED de origen.
        evaluaciones_realizadas: Lista de tamizajes o evaluaciones completadas.
        nivel_riesgo_actual: Nivel de riesgo ('BAJO', 'MODERADO', 'ALTO').

    Returns:
        Diccionario estructurado con la Ficha Clínica Multidisciplinaria.
    """
    resumen_id = f"RES-NEURO-{uuid.uuid4().hex[:6].upper()}"
    fecha = datetime.now().strftime("%Y-%m-%d")

    return {
        "resumen_id": resumen_id,
        "fecha_consolidado": fecha,
        "paciente": {
            "nombre": nombre_paciente,
            "edad_meses": edad_meses,
        },
        "historial_cred": antecedentes_cred,
        "evaluaciones_previas": evaluaciones_realizadas,
        "nivel_riesgo_actual": nivel_riesgo_actual,
        "equipo_multidisciplinario_sugerido": [
            "Neuropediatría / Psiquiatría Infantil",
            "Psicología Infantil",
            "Terapia del Lenguaje",
            "Terapia Ocupacional / Física",
        ],
        "estado_resumen": "CONSOLIDADO_LISTO_PARA_CONSULTA",
    }
