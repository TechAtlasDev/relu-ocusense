import pytest
from app.tools.tamizaje import evaluar_tamizaje_oximetria, calcular_sat_fisiologica


def test_calcular_sat_fisiologica():
    # Nivel del mar (Lima)
    assert calcular_sat_fisiologica(100) == 97.0
    
    # Altitud moderada (Arequipa ~2300m)
    sat_arequipa = calcular_sat_fisiologica(2300)
    assert 94.0 <= sat_arequipa <= 96.0

    # Gran altitud (Juliaca ~3825m)
    sat_juliaca = calcular_sat_fisiologica(3825)
    assert 88.0 <= sat_juliaca < 92.0


def test_evaluar_tamizaje_normal_costa():
    result = evaluar_tamizaje_oximetria.invoke({
        "sat_mano_derecha": 98.0,
        "sat_pie": 97.0,
        "msnm": 100
    })
    assert "ESTADO_TAMIZAJE: NEGATIVO" in result


def test_evaluar_tamizaje_positivo_juliaca_por_bajo_corte():
    # En Juliaca (3825m), una saturación de 85% está por debajo del rango fisiológico normal ajustado
    result = evaluar_tamizaje_oximetria.invoke({
        "sat_mano_derecha": 85.0,
        "sat_pie": 86.0,
        "msnm": 3825
    })
    assert "ESTADO_TAMIZAJE: POSITIVO" in result
    assert "activar tele-interconsulta urgente con INSN-SB" in result


def test_evaluar_tamizaje_positivo_por_diferencial():
    # Mano 95%, Pie 90% (diferencia >3%) -> Positivo por gradiente
    result = evaluar_tamizaje_oximetria.invoke({
        "sat_mano_derecha": 95.0,
        "sat_pie": 90.0,
        "msnm": 100
    })
    assert "ESTADO_TAMIZAJE: POSITIVO" in result


def test_evaluar_tamizaje_dudoso():
    # Resultado en límite que exige repetir en 1 hora
    result = evaluar_tamizaje_oximetria.invoke({
        "sat_mano_derecha": 94.0,
        "sat_pie": 94.0,
        "msnm": 100
    })
    assert "ESTADO_TAMIZAJE: DUDOSO" in result
    assert "Repetir tamizaje de oximetría en 1 hora" in result

