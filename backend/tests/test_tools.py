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
    assert len(tools) == 5
    names = [t.name for t in tools]
    assert "calculate_expression" in names
    assert "get_current_time" in names
    assert "evaluar_tamizaje_oximetria" in names
    assert "emitir_alerta_teleinterconsulta_insn" in names
    assert "generar_ficha_referencia_sis" in names


