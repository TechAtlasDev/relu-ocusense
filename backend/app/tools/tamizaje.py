from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class TamizajeResult(BaseModel):
    resultado: Literal["POSITIVO", "NEGATIVO", "DUDOSO"] = Field(
        ..., description="Resultado del tamizaje: POSITIVO (Sospecha CCC), NEGATIVO (Normal) o DUDOSO (Repetir en 1 hora)"
    )
    sat_fisiologica_esperada: float = Field(
        ..., description="Saturación fisiológica base calculada según la altitud en m.s.n.m."
    )
    diferencial_observado: float = Field(
        ..., description="Diferencia absoluta entre la mano derecha (pre-ductal) y el pie (post-ductal)"
    )
    mensaje_clinico: str = Field(
        ..., description="Recomendación y conducta médica a seguir inmediatamente"
    )


def calcular_sat_fisiologica(msnm: int) -> float:
    """
    Estima la saturación media fisiológica neonatal normal según la altitud en metros sobre el nivel del mar.
    - A nivel del mar (<1000m): ~97-98%
    - Altitud moderada (1000-2500m): ~94-96%
    - Gran altitud (>2500m - ej. Puno, Cusco, Juliaca): ~89-93%
    """
    if msnm < 1000:
        return 97.0
    elif msnm <= 2500:
        # Decremento gradual aproximado
        return max(94.0, 97.0 - ((msnm - 1000) / 1500) * 3.0)
    else:
        # Gran altitud (Sierra)
        decremento = ((msnm - 2500) / 1500) * 4.0
        return max(88.0, 94.0 - decremento)


@tool
def evaluar_tamizaje_oximetria(
    sat_mano_derecha: float,
    sat_pie: float,
    msnm: int = 0,
    edad_horas: int = 24
) -> str:
    """
    Evalúa el tamizaje neonatal de oximetría de pulso (pre-ductal mano derecha y post-ductal pie) 
    adaptando los umbrales fisiológicos de corte según la altitud en m.s.n.m. para el entorno peruano.
    
    Parámetros:
      - sat_mano_derecha: Saturación medida en la mano derecha (pre-ductal, 0-100%).
      - sat_pie: Saturación medida en cualquiera de los pies (post-ductal, 0-100%).
      - msnm: Altitud en metros sobre el nivel del mar de la localidad del centro de salud (ej. Juliaca: 3825, Cusco: 3400, Lima: 100).
      - edad_horas: Edad del recién nacido en horas (idealmente entre 12 y 48 horas post-parto).
    """
    if sat_mano_derecha < 0 or sat_mano_derecha > 100 or sat_pie < 0 or sat_pie > 100:
        return "Error: Los valores de saturación deben estar entre 0% y 100%."

    sat_esperada = calcular_sat_fisiologica(msnm)
    diferencial = abs(sat_mano_derecha - sat_pie)
    
    # Umbral de corte ajustado por altitud
    # Si la altitud es elevada (>2500m), la saturación normal es menor, pero un valor <88% o diferencial >3% sigue siendo sospechoso.
    corte_minimo = max(88.0, sat_esperada - 4.0)

    es_positivo = (
        sat_mano_derecha < corte_minimo or 
        sat_pie < corte_minimo or 
        diferencial > 3.0
    )
    
    es_dudoso = (
        not es_positivo and (
            (sat_mano_derecha < (corte_minimo + 2.0)) or 
            (sat_pie < (corte_minimo + 2.0)) or 
            (diferencial == 3.0)
        )
    )

    if es_positivo:
        resultado = "POSITIVO"
        conducta = "Sospecha de Cardiopatía Congénita Crítica (CCC). Requiere observación, mantener normotérmico y activar tele-interconsulta urgente con INSN-SB."
    elif es_dudoso:
        resultado = "DUDOSO"
        conducta = "Resultado en zona límite. No dar de alta. Repetir tamizaje de oximetría en 1 hora."
    else:
        resultado = "NEGATIVO"
        conducta = "Valores dentro de rangos fisiológicos normales ajustados por altitud. Continuar con protocolo estándar de alta."

    return (
        f"ESTADO_TAMIZAJE: {resultado}\n"
        f"ALTITUD: {msnm} m.s.n.m. (Saturación base esperada: {sat_esperada:.1f}%)\n"
        f"MEDICIONES: Mano Der={sat_mano_derecha}%, Pie={sat_pie}%, Gradiente={diferencial:.1f}%\n"
        f"RECOMENDACION_TECNICA: {conducta}"
    )
