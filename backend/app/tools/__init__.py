from langchain_core.tools import BaseTool
from .calculator import calculate_expression
from .time_tool import get_current_time
from .tamizaje import evaluar_tamizaje_oximetria
from .referencia import emitir_alerta_teleinterconsulta_insn, generar_ficha_referencia_sis


def get_all_tools() -> list[BaseTool]:
    """Retorna la lista centralizada de todas las herramientas registradas para ReLU."""
    return [
        calculate_expression,
        get_current_time,
        evaluar_tamizaje_oximetria,
        emitir_alerta_teleinterconsulta_insn,
        generar_ficha_referencia_sis,
    ]


