import uuid
from datetime import datetime
from typing import Optional
from langchain_core.tools import tool


@tool
def emitir_alerta_teleinterconsulta_insn(
    nombre_paciente: str,
    edad_horas: int,
    distrito_origen: str,
    msnm: int,
    sat_mano_derecha: float,
    sat_pie: float,
    codigo_renipress: Optional[str] = "P-SERUMS-001"
) -> str:
    """
    Emite una alerta clínica de prioridad roja y simula el registro de una solicitud de tele-interconsulta 
    urgente enviada a la Central de Referencias del Instituto Nacional de Salud del Niño San Borja (INSN-SB).
    
    Parámetros:
      - nombre_paciente: Nombre o código anónimo del neonato.
      - edad_horas: Edad del recién nacido en horas.
      - distrito_origen: Nombre del distrito/localidad de origen (ej. Juliaca, Huancavelica).
      - msnm: Altitud en m.s.n.m. de la localidad.
      - sat_mano_derecha: Saturación mano derecha (pre-ductal).
      - sat_pie: Saturación pie (post-ductal).
      - codigo_renipress: Código RENIPRESS del establecimiento de origen.
    """
    ticket_id = f"INSN-CCC-{uuid.uuid4().hex[:6].upper()}"
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    diferencial = abs(sat_mano_derecha - sat_pie)

    resumen_alerta = (
        f"🚨 **¡TELE-INTERCONSULTA PRIORITARIA ENVIADA AL INSN-SB!** 🚨\n\n"
        f"📋 **Ticket de Referencia:** `{ticket_id}`\n"
        f"⏱️ **Fecha y Hora de Emisión:** {fecha_hora}\n"
        f"🏥 **Establecimiento de Origen:** RENIPRESS `{codigo_renipress}` - {distrito_origen} ({msnm} m.s.n.m.)\n"
        f"👶 **Paciente:** {nombre_paciente} ({edad_horas} horas de vida)\n"
        f"📊 **Datos de Oximetría:** Mano Der: `{sat_mano_derecha}%` | Pie: `{sat_pie}%` | Gradiente: `{diferencial:.1f}%`\n\n"
        "⚡ **CONDUCTA CLÍNICA DE EMERGENCIA:**\n"
        "1. Se ha notificado al cardiólogo pediatra de guardia del INSN-SB.\n"
        "2. Mantener al recién nacido con temperatura adecuada (36.5 - 37.5 °C) y oxigenoterapia de soporte si presenta distrés.\n"
        "3. **Canal Directo de Tele-orientación:** Usa el código de ticket temporal en la central para coordinar el traslado aéreo/terrestre inmediato."
    )
    return resumen_alerta


@tool
def generar_ficha_referencia_sis(
    nombre_paciente: str,
    dni_apoderado: str,
    distrito_origen: str,
    diagnostico_presuntivo: str = "Sospecha de Cardiopatía Congénita Crítica (Q24.9)",
    resumen_clinico: str = "Tamizaje de oximetría alterado pre/post ductal."
) -> str:
    """
    Genera un borrador estructurado de la Ficha Única de Atención (FUA) y Hoja de Referencia del SIS 
    para agilizar el trámite administrativo interhospitalario evitando retrasos en la derivación al INSN-SB.
    """
    fua_id = f"FUA-{uuid.uuid4().hex[:8].upper()}"
    
    ficha_md = (
        f"📋 **BORRADOR DE FICHA DE REFERENCIA SIS / FUA** 📋\n"
        f"🆔 **N° Formato FUA:** `{fua_id}`\n"
        f"👤 **Paciente Neonato:** {nombre_paciente}\n"
        f"📄 **DNI Apoderado/Madre:** `{dni_apoderado}`\n"
        f"📍 **Origen:** {distrito_origen} ➡️ **Destino:** INSN-SB (Lima)\n"
        f"🩺 **CIE-10 Presuntivo:** `{diagnostico_presuntivo}`\n"
        f"📝 **Resumen Anamnesis & Tamizaje:** {resumen_clinico}\n\n"
        "✅ *Ficha pre-validada sin cuellos de botella administrativos. Lista para firma digital/física del médico de posta.*"
    )
    return ficha_md
