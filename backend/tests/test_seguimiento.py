from app.tools.seguimiento import programar_seguimiento_cita, obtener_plan_refuerzo_hogar


def test_programar_seguimiento_cita():
    res = programar_seguimiento_cita.invoke({
        "fecha_proxima_cita": "2026-09-15",
        "especialidad": "Terapia de Lenguaje",
        "frecuencia_terapia_semanal": 2,
    })
    assert res["especialidad"] == "Terapia de Lenguaje"
    assert res["fecha_cita"] == "2026-09-15"
    assert len(res["recordatorios_programados"]) == 2
    assert len(res["estrategias_adherencia"]) == 3


def test_obtener_plan_refuerzo_hogar_tea():
    res = obtener_plan_refuerzo_hogar.invoke({
        "condicion_suspecta": "TEA",
        "edad_meses": 30,
    })
    assert res["condicion_suspecta"] == "TEA"
    assert len(res["actividades_recomendadas"]) >= 3
    assert "pictogramas" in res["actividades_recomendadas"][0].lower()


def test_obtener_plan_refuerzo_hogar_lenguaje():
    res = obtener_plan_refuerzo_hogar.invoke({
        "condicion_suspecta": "Retraso_Lenguaje",
        "edad_meses": 24,
    })
    assert "lenguaje" in res["condicion_suspecta"].lower()
    assert len(res["actividades_recomendadas"]) >= 3
