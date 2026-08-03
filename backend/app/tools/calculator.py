from langchain_core.tools import tool


@tool
def calculate_expression(expression: str) -> str:
    """Calcula el resultado matemático de una expresión aritmética. Úsalo para operaciones numéricas o cálculos matemáticos."""
    try:
        # Evaluación segura de expresiones aritméticas simples
        allowed_names = {"abs": abs, "round": round, "pow": pow}
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return f"Resultado de la operación '{expression}': {result}"
    except Exception as err:
        return f"No se pudo evaluar la expresión '{expression}'. Error: {err}"
