from app.tools.neuro_tamizaje import evaluar_desarrollo_infantil


def test_evaluar_desarrollo_infantil_alto_riesgo():
    res = evaluar_desarrollo_infantil.invoke({
        "edad_meses": 24,
        "senales_observadas": ["contacto visual nulo", "sin lenguaje a los 24m", "ecolalia"],
        "rol_usuario": "personal_salud",
    })
    assert res["nivel_riesgo"] == "ALTO"
    assert res["requiere_referencia"] is True
    assert "M-CHAT-R/F" in res["escala_usada"]
    assert "prioritaria" in res["recomendacion"].lower()


def test_evaluar_desarrollo_infantil_moderado_riesgo():
    res = evaluar_desarrollo_infantil.invoke({
        "edad_meses": 48,
        "senales_observadas": ["inatencion", "rabieta frecuente"],
        "rol_usuario": "familia",
    })
    assert res["nivel_riesgo"] == "MODERADO"
    assert res["requiere_referencia"] is True
    assert "3-5a" in res["escala_usada"]


def test_evaluar_desarrollo_infantil_bajo_riesgo():
    res = evaluar_desarrollo_infantil.invoke({
        "edad_meses": 12,
        "senales_observadas": ["juega tranquilo", "sonríe al llamado"],
        "rol_usuario": "personal_salud",
    })
    assert res["nivel_riesgo"] == "BAJO"
    assert res["requiere_referencia"] is False
    assert "CRED" in res["recomendacion"]
