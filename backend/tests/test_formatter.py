"""
Tests para app.utils.formatter — conversión de Markdown estándar a MarkdownV2 de Telegram.
"""
import pytest
from app.utils.formatter import markdown_to_telegram_v2, sanitize_markdown


# ---------------------------------------------------------------------------
# Texto plano — caracteres reservados de MarkdownV2 deben escaparse
# ---------------------------------------------------------------------------

def test_plain_text_escapes_dot():
    result = markdown_to_telegram_v2("Hola mundo.")
    assert result == r"Hola mundo\."


def test_plain_text_escapes_exclamation():
    result = markdown_to_telegram_v2("Hola!")
    assert result == r"Hola\!"


def test_plain_text_escapes_parentheses():
    result = markdown_to_telegram_v2("valor (msnm)")
    assert result == r"valor \(msnm\)"


def test_plain_text_escapes_hyphen():
    result = markdown_to_telegram_v2("pre-ductal")
    assert result == r"pre\-ductal"


def test_emoji_preserved():
    result = markdown_to_telegram_v2("Hola 👋 mundo 🚀")
    assert "👋" in result
    assert "🚀" in result


# ---------------------------------------------------------------------------
# Encabezados
# ---------------------------------------------------------------------------

def test_h3_converts_to_bold():
    result = markdown_to_telegram_v2("### Mi Título")
    assert result == "*Mi Título*"


def test_h1_converts_to_bold():
    result = markdown_to_telegram_v2("# Título Principal")
    assert result == "*Título Principal*"


def test_header_with_bold_inside_strips_markers():
    result = markdown_to_telegram_v2("#### **Paso 1: Datos**")
    assert result.startswith("*")
    assert "Paso 1" in result
    # Los ** internos no deben duplicarse
    assert "**" not in result


def test_header_with_special_chars_escapes_correctly():
    result = markdown_to_telegram_v2("### Flujo en 4 Pasos:")
    # El ":" no es reservado en MDv2, pero los demás chars sí
    assert result == "*Flujo en 4 Pasos:*"


# ---------------------------------------------------------------------------
# Negrita e Itálica
# ---------------------------------------------------------------------------

def test_bold_converts():
    result = markdown_to_telegram_v2("Texto **negrita** aquí")
    assert "*negrita*" in result


def test_italic_converts():
    result = markdown_to_telegram_v2("Texto *cursiva* aquí")
    assert "_cursiva_" in result


def test_bold_italic_converts():
    result = markdown_to_telegram_v2("Texto ***negcurs*** aquí")
    assert "*_negcurs_*" in result


def test_bullet_asterisk_not_converted_to_italic():
    """Un '* item' de lista no debe convertirse en itálica."""
    result = markdown_to_telegram_v2("* primer ítem\n* segundo ítem")
    # El * al inicio de línea debe estar escapado, no ser itálica
    assert "_primer" not in result
    assert r"\*" in result or "\\*" in result


# ---------------------------------------------------------------------------
# Separadores horizontales
# ---------------------------------------------------------------------------

def test_horizontal_rule_converts():
    result = markdown_to_telegram_v2("Texto\n\n---\n\nMás texto")
    assert "---" not in result
    assert "—" in result


# ---------------------------------------------------------------------------
# LaTeX
# ---------------------------------------------------------------------------

def test_latex_inline_converts_to_code():
    result = markdown_to_telegram_v2("La fórmula $\\Delta > 3\\%$ es clave")
    assert "`\\Delta > 3\\%`" in result


def test_latex_paren_converts_to_code():
    result = markdown_to_telegram_v2("Resultado: \\(x + y\\) es válido")
    assert "`x + y`" in result


# ---------------------------------------------------------------------------
# Bloques de código
# ---------------------------------------------------------------------------

def test_code_block_preserved():
    text = "```python\ndef hola():\n    pass\n```"
    result = markdown_to_telegram_v2(text)
    assert "```python" in result
    assert "def hola():" in result


def test_code_block_content_not_escaped():
    """El contenido de un bloque de código NO debe tener escapes de MDv2."""
    text = "```\nvalor = 3.14\n```"
    result = markdown_to_telegram_v2(text)
    # El punto dentro del bloque no debe escaparse
    assert "3.14" in result
    assert r"3\.14" not in result


def test_inline_code_preserved():
    result = markdown_to_telegram_v2("Usa `git status` para ver cambios")
    assert "`git status`" in result


def test_inline_code_content_not_escaped():
    """El contenido de código inline NO debe escaparse."""
    result = markdown_to_telegram_v2("El flag `--timeout=60` es clave")
    assert "`--timeout=60`" in result
    assert r"`\-\-timeout\=60`" not in result


# ---------------------------------------------------------------------------
# Tachado
# ---------------------------------------------------------------------------

def test_strikethrough_converts():
    result = markdown_to_telegram_v2("Texto ~~tachado~~ aquí")
    assert "~tachado~" in result


# ---------------------------------------------------------------------------
# Links
# ---------------------------------------------------------------------------

def test_link_converts():
    result = markdown_to_telegram_v2("[Google](https://google.com)")
    assert "[Google]" in result
    assert "https://google.com" in result


# ---------------------------------------------------------------------------
# Texto vacío y alias de compatibilidad
# ---------------------------------------------------------------------------

def test_empty_string_returns_empty():
    assert markdown_to_telegram_v2("") == ""


def test_none_like_empty_handled():
    assert markdown_to_telegram_v2("") == ""


def test_sanitize_markdown_alias():
    """sanitize_markdown es alias de markdown_to_telegram_v2."""
    text = "### Hola"
    assert sanitize_markdown(text) == markdown_to_telegram_v2(text)


# ---------------------------------------------------------------------------
# Caso de integración — respuesta real del LLM
# ---------------------------------------------------------------------------

def test_full_llm_response_does_not_crash():
    """Una respuesta larga y compleja del LLM debe convertirse sin excepciones."""
    sample = """\
### El Flujo de Trabajo en 4 Pasos:

```
1. Ingreso ➔ 2. Evaluación ➔ 3. Resultado ➔ 4. Alerta
```

#### **Paso 1: Recolección de Datos** 📝
El personal proporciona 4 datos:
1. **Saturación Mano Derecha** (Pre-ductal).
2. **Saturación en Pie** (Post-ductal).

#### **Paso 2: Evaluación** 🏔️
Calcula la diferencia ($\\Delta > 3\\%$).

---

### ¿Hacemos una prueba en vivo?
"""
    result = markdown_to_telegram_v2(sample)
    assert isinstance(result, str)
    assert len(result) > 0
    # Los headers deben estar en negrita
    assert "*El Flujo de Trabajo en 4 Pasos" in result
    # El bloque de código debe estar intacto
    assert "```" in result
    # Los separadores deben convertirse
    assert "---" not in result
