import uuid
from datetime import datetime
from langchain_core.tools import tool


@tool
def emitir_referencia_neurodesarrollo(
    nombre_paciente: str,
    edad_meses: int,
    nivel_riesgo: str,
    especialidad_destino: str,
    establecimiento_origen: str,
    resumen_clinico: str,
) -> dict:
    """Emite una solicitud de tele-referencia o interconsulta para evaluación multidisciplinaria en neurodesarrollo.

    Args:
        nombre_paciente: Nombre o iniciales del paciente.
        edad_meses: Edad en meses del paciente.
        nivel_riesgo: Nivel de riesgo determinado ('BAJO', 'MODERADO', 'ALTO').
        especialidad_destino: Especialidad requerida ('Neuropediatría', 'Psiquiatría Infantil', 'Psicología', 'Terapia de Lenguaje', 'Terapia Ocupacional').
        establecimiento_origen: Centro de salud o establecimiento de origen.
        resumen_clinico: Breve descripción de las señales de alarma observadas.

    Returns:
        Un diccionario estructurado con los detalles del ticket de tele-referencia.
    """
    ticket_id = f"REF-NEURO-{uuid.uuid4().hex[:6].upper()}"
    fecha_emision = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prioridad = "PRIORITARIA" if nivel_riesgo == "ALTO" else "REGULAR"

    return {
        "ticket_id": ticket_id,
        "fecha_emision": fecha_emision,
        "nombre_paciente": nombre_paciente,
        "edad_meses": edad_meses,
        "nivel_riesgo": nivel_riesgo,
        "prioridad": prioridad,
        "especialidad_destino": especialidad_destino,
        "establecimiento_origen": establecimiento_origen,
        "resumen_clinico": resumen_clinico,
        "estado": "EMITIDO_PENDIENTE_CITACION",
        "mensaje": f"Referencia {ticket_id} generada exitosamente hacia {especialidad_destino}.",
    }


@tool
def generar_ficha_fua_neurodesarrollo(
    diagnostico_presuntivo: str,
    cod_cie10: str,
    atencion_cred: bool = True,
) -> dict:
    """Genera el borrador del Formato Único de Atención (FUA/SIS) para trastornos del neurodesarrollo.

    Args:
        diagnostico_presuntivo: Descripción del diagnóstico o sospecha (ej. 'Sospecha de Trastorno del Espectro Autista').
        cod_cie10: Código CIE-10 asignado (ej. 'F84.0', 'F90.0', 'F80.1', 'R62.0').
        atencion_cred: Indica si la atención se realiza en el marco del control CRED.

    Returns:
        Diccionario estructurado con los campos de la ficha FUA/SIS.
    """
    fua_id = f"FUA-SIS-{uuid.uuid4().hex[:8].upper()}"
    
    codigo_servicio = "011" if atencion_cred else "056"
    nombre_servicio = "CRED - Crecimiento y Desarrollo" if atencion_cred else "Consulta Externa Pediatría/Psicología"

    return {
        "fua_id": fua_id,
        "servicio_prestacion": nombre_servicio,
        "codigo_servicio": codigo_servicio,
        "diagnostico_presuntivo": diagnostico_presuntivo,
        "cie10": cod_cie10,
        "cobertura_sis": "100% Cubierto",
        "estado_ficha": "BORRADOR_LISTO_PARA_FIRMA",
        "instrucciones": "Adjuntar ficha FUA a la solicitud de referencia física o digital del establecimiento.",
    }
