from datetime import datetime
from langchain_core.tools import tool


@tool
def get_current_time(timezone_str: str = "UTC") -> str:
    """Obtiene la fecha y hora actual en tiempo real. Úsalo cuando el usuario te pregunte qué hora es o la fecha de hoy."""
    now = datetime.now()
    return f"La fecha y hora actual es: {now.strftime('%Y-%m-%d %H:%M:%S')} ({timezone_str})"
