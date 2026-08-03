from app.utils.formatter import sanitize_markdown


def test_sanitize_markdown_code_block_balancing():
    text_unclosed = "Aquí hay código:\n```python\ndef hola():\n    print('hola')"
    sanitized = sanitize_markdown(text_unclosed)
    assert sanitized.count("```") % 2 == 0
    assert sanitized.endswith("\n```")


def test_sanitize_markdown_inline_code_balancing():
    text_unclosed = "Usa el comando `git status para ver cambios"
    sanitized = sanitize_markdown(text_unclosed)
    assert sanitized.count("`") % 2 == 0


def test_sanitize_markdown_emoji_preservation():
    text_with_emoji = "Hola 👋 este es un mensaje 🚀 de prueba"
    sanitized = sanitize_markdown(text_with_emoji)
    assert "👋" in sanitized
    assert "🚀" in sanitized

