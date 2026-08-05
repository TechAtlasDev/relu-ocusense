from app.tools.neuro_referencia import emitir_referencia_neurodesarrollo, generar_ficha_fua_neurodesarrollo


def test_emitir_referencia_neurodesarrollo():
    res = emitir_referencia_neurodesarrollo.invoke({
        "nombre_paciente": "J.P.",
        "edad_meses": 24,
        "nivel_riesgo": "ALTO",
        "especialidad_destino": "Neuropediatría",
        "establecimiento_origen": "CS San Juan de Lurigancho",
        "resumen_clinico": "Ausencia de lenguaje y contacto visual.",
    })
    assert res["ticket_id"].startswith("REF-NEURO-")
    assert res["prioridad"] == "PRIORITARIA"
    assert res["especialidad_destino"] == "Neuropediatría"
    assert res["estado"] == "EMITIDO_PENDIENTE_CITACION"


def test_generar_ficha_fua_neurodesarrollo():
    res = generar_ficha_fua_neurodesarrollo.invoke({
        "diagnostico_presuntivo": "Trastorno del Espectro Autista",
        "cod_cie10": "F84.0",
        "atencion_cred": True,
    })
    assert res["fua_id"].startswith("FUA-SIS-")
    assert res["cie10"] == "F84.0"
    assert res["codigo_servicio"] == "011"
    assert res["cobertura_sis"] == "100% Cubierto"
