from langchain_core.tools import BaseTool
from .calculator import calculate_expression
from .time_tool import get_current_time
from .neuro_tamizaje import evaluar_desarrollo_infantil
from .neuro_referencia import emitir_referencia_neurodesarrollo, generar_ficha_fua_neurodesarrollo
from .seguimiento import programar_seguimiento_cita, obtener_plan_refuerzo_hogar
from .historia import generar_resumen_caso_multidisciplinario


def get_all_tools() -> list[BaseTool]:
    """Retorna la lista centralizada de todas las herramientas registradas para ReLU (Neuroalianza)."""
    return [
        calculate_expression,
        get_current_time,
        evaluar_desarrollo_infantil,
        emitir_referencia_neurodesarrollo,
        generar_ficha_fua_neurodesarrollo,
        programar_seguimiento_cita,
        obtener_plan_refuerzo_hogar,
        generar_resumen_caso_multidisciplinario,
    ]
