import pytest
from app.tools.calculator import calculate_expression
from app.tools.time_tool import get_current_time
from app.tools import get_all_tools


def test_calculate_expression_tool():
    res = calculate_expression.invoke({"expression": "25 * 4"})
    assert "100" in res


def test_get_current_time_tool():
    res = get_current_time.invoke({"timezone_str": "UTC"})
    assert "fecha y hora actual" in res.lower()


def test_get_all_tools_registration():
    tools = get_all_tools()
    assert len(tools) == 8
    names = [t.name for t in tools]
    assert "calculate_expression" in names
    assert "get_current_time" in names
    assert "evaluar_desarrollo_infantil" in names
    assert "emitir_referencia_neurodesarrollo" in names
    assert "generar_ficha_fua_neurodesarrollo" in names
    assert "programar_seguimiento_cita" in names
    assert "obtener_plan_refuerzo_hogar" in names
    assert "generar_resumen_caso_multidisciplinario" in names
