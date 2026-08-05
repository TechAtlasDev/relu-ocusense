from app.tools.historia import generar_resumen_caso_multidisciplinario


def test_generar_resumen_caso_multidisciplinario():
    res = generar_resumen_caso_multidisciplinario.invoke({
        "nombre_paciente": "M.G.",
        "edad_meses": 36,
        "antecedentes_cred": "Control CRED a los 36m muestra retraso en área de lenguaje e interacción.",
        "evaluaciones_realizadas": ["M-CHAT-R/F Riesgo Alto", "Cuestionario de Lenguaje"],
        "nivel_riesgo_actual": "ALTO",
    })
    assert res["resumen_id"].startswith("RES-NEURO-")
    assert res["paciente"]["nombre"] == "M.G."
    assert res["nivel_riesgo_actual"] == "ALTO"
    assert len(res["equipo_multidisciplinario_sugerido"]) >= 3
    assert res["estado_resumen"] == "CONSOLIDADO_LISTO_PARA_CONSULTA"
