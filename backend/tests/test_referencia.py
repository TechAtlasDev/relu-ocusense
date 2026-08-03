import pytest
from app.tools.referencia import emitir_alerta_teleinterconsulta_insn, generar_ficha_referencia_sis


def test_emitir_alerta_teleinterconsulta_insn():
    result = emitir_alerta_teleinterconsulta_insn.invoke({
        "nombre_paciente": "Bebé Quispe",
        "edad_horas": 24,
        "distrito_origen": "Juliaca",
        "msnm": 3825,
        "sat_mano_derecha": 85.0,
        "sat_pie": 86.0
    })
    assert "TELE-INTERCONSULTA PRIORITARIA ENVIADA AL INSN-SB" in result
    assert "INSN-CCC-" in result
    assert "Juliaca" in result


def test_generar_ficha_referencia_sis():
    result = generar_ficha_referencia_sis.invoke({
        "nombre_paciente": "Bebé Quispe",
        "dni_apoderado": "70654321",
        "distrito_origen": "Juliaca"
    })
    assert "BORRADOR DE FICHA DE REFERENCIA SIS / FUA" in result
    assert "FUA-" in result
    assert "70654321" in result
