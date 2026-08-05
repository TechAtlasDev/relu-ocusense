from langchain_core.tools import tool


@tool
def evaluar_desarrollo_infantil(edad_meses: int, senales_observadas: list[str], rol_usuario: str = "personal_salud") -> dict:
    """Evalúa el desarrollo infantil y nivel de riesgo de trastornos del neurodesarrollo (TEA, TDAH, retraso del lenguaje/motor).

    Args:
        edad_meses: Edad del niño en meses (ejemplo: 18 para 1 año y medio, 48 para 4 años).
        senales_observadas: Lista de síntomas o comportamientos observados (ejemplo: ['falta contacto visual', 'no responde al nombre', 'sin lenguaje a los 24m']).
        rol_usuario: Rol de la persona que consulta ('personal_salud' o 'familia').

    Returns:
        Un diccionario estructurado con la clasificación de riesgo, herramienta de tamizaje usada y conducta sugerida.
    """
    senales_clean = [s.lower().strip() for s in senales_observadas]
    
    # Marcadores de alto riesgo
    alto_riesgo_keywords = [
        "perdida de habilidades", "ecolalia", "marcha en puntillas", "contacto visual nulo",
        "falta de sonrisa social", "sin balbuceo", "sin lenguaje", "autolesion", "hiperactividad severa",
        "no responde a su nombre", "no senala", "aislamiento", "crisis sensoriales"
    ]
    
    # Marcadores de riesgo moderado
    moderado_riesgo_keywords = [
        "inatencion", "rabieta frecuente", "dificultad para coordinar", "torpeza motora",
        "vocabulario reducido", "lenguaje poco claro", "desobediencia", "inquietud"
    ]
    
    score_alto = sum(1 for kw in alto_riesgo_keywords if any(kw in s for s in senales_clean))
    score_moderado = sum(1 for kw in moderado_riesgo_keywords if any(kw in s for s in senales_clean))
    
    if edad_meses <= 30:
        escala_usada = "M-CHAT-R/F y EEDP/TPED (CRED 0-30m)"
    elif edad_meses <= 60:
        escala_usada = "Evaluación de Hitos del Desarrollo y Lenguaje (3-5a)"
    else:
        escala_usada = "Criterios Vanderbilt / Conners para Neurodesarrollo (6-17a)"
        
    if score_alto >= 2 or len(senales_observadas) >= 4:
        nivel_riesgo = "ALTO"
        recomendacion = (
            "Se identifica una alta probabilidad de alteración en el neurodesarrollo. "
            "Se requiere derivación prioritaria a evaluación multidisciplinaria (Neuropediatría / Psiquiatría Infantil / Psicología)."
        )
        requiere_referencia = True
    elif score_alto == 1 or score_moderado >= 2:
        nivel_riesgo = "MODERADO"
        recomendacion = (
            "Se identifican señales de alarma moderadas. Se recomienda re-evaluación en 30 días, "
            "evaluación por psicología/pediatría y pautas de estimulación focalizada en el hogar."
        )
        requiere_referencia = True
    else:
        nivel_riesgo = "BAJO"
        recomendacion = (
            "No se identifican señales de alarma críticas actuales. "
            "Mantener controles periódicos en el programa CRED y pautas habituales de estimulación."
        )
        requiere_referencia = False
        
    return {
        "edad_meses": edad_meses,
        "escala_usada": escala_usada,
        "nivel_riesgo": nivel_riesgo,
        "senales_evaluadas": senales_observadas,
        "requiere_referencia": requiere_referencia,
        "recomendacion": recomendacion,
    }
