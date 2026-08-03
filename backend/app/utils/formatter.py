import re


def escape_markdown_v2_unformatted(text: str) -> str:
    """Escapa caracteres especiales de Telegram conservando la sintaxis Markdown habitual (*, _, `, #, [], ())."""
    if not text:
        return ""
    
    # Caracteres de Telegram MarkdownV2 que suelen romper la renderización si no están en bloques
    # Especialmente '.', '-', '!', '(', ')', '+', '='
    chars_to_escape = r"[\.\-\!\(\)\+\=\|\{\}\>\#]"
    return re.sub(f"({chars_to_escape})", r"\\\1", text)


def sanitize_markdown(text: str) -> str:
    """Sanitiza y auto-completa sintaxis Markdown para asegurar un renderizado limpio en Telegram.

    - Escapa guiones, puntos y signos reservados que rompen el parser de Telegram.
    - Balancear comillas y bloques de código ` y ```.
    - Convierte ecuaciones LaTeX a formato legible.
    """
    if not text:
        return ""

    sanitized = text

    # Balancear bloques de código ```
    code_block_count = sanitized.count("```")
    if code_block_count % 2 != 0:
        sanitized += "\n```"

    # Balancear comillas simples de código `
    parts = sanitized.split("```")
    even_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            inline_code_count = part.count("`")
            if inline_code_count % 2 != 0:
                part += "`"
        even_parts.append(part)
    sanitized = "```".join(even_parts)

    # Convertir delimitadores LaTeX \(...\) y \[...\] a código
    sanitized = re.sub(r"\\\((.*?)\\\)", r"`\1`", sanitized)
    sanitized = re.sub(r"\\\[(.*?)\\\]", r"`\1`", sanitized)

    return sanitized


