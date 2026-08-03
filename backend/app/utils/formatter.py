import re


def _escape_plain(text: str) -> str:
    """Escapa todos los caracteres reservados de MarkdownV2 en texto plano.

    Caracteres reservados según la documentación de Telegram:
    _ * [ ] ( ) ~ ` > # + - = | { } . !
    """
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', text)


def _convert_non_code(text: str) -> str:
    """
    Convierte un segmento de texto plano (sin bloques de código)
    de Markdown estándar a MarkdownV2 de Telegram.

    Orden de procesamiento (importa para evitar colisiones):
    1. Headers  →  bold
    2. Horizontal rules  →  separador visual
    3. LaTeX  →  inline code
    4. Bold+Italic  →  *_text_*
    5. Bold  →  *text*
    6. Italic  →  _text_
    7. Strikethrough  →  ~text~
    8. Links  →  [text](url)
    9. Escapa el resto del texto plano
    """
    phs: dict[str, str] = {}
    counter = [0]

    def _ph() -> str:
        key = f"\x00{counter[0]}\x00"
        counter[0] += 1
        return key

    # 1. Headers: # ... → *bold*
    def _header(m: re.Match) -> str:
        content = m.group(2).strip()
        # Eliminar marcadores inline de la cabecera antes de escapar
        content = re.sub(r"\*+([^*]+)\*+", r"\1", content)
        content = re.sub(r"_+([^_]+)_+", r"\1", content)
        key = _ph()
        phs[key] = f"*{_escape_plain(content)}*"
        return key

    text = re.sub(r"^(#{1,6})\s+(.+)$", _header, text, flags=re.MULTILINE)

    # 2. Horizontal rules: --- / *** / ___ → separador visual
    text = re.sub(
        r"^\s*(\-{3,}|\*{3,}|_{3,})\s*$",
        "—————————",
        text,
        flags=re.MULTILINE,
    )

    # 3. LaTeX: $...$  \(...\)  \[...\] → inline code
    def _latex(expr: str) -> str:
        key = _ph()
        phs[key] = f"`{expr}`"
        return key

    text = re.sub(r"\$([^$\n]+)\$", lambda m: _latex(m.group(1)), text)
    text = re.sub(
        r"\\\((.+?)\\\)", lambda m: _latex(m.group(1)), text, flags=re.DOTALL
    )
    text = re.sub(
        r"\\\[(.+?)\\\]", lambda m: _latex(m.group(1)), text, flags=re.DOTALL
    )

    # 4. Bold+Italic: ***text*** → *_text_*
    def _bold_italic(m: re.Match) -> str:
        key = _ph()
        phs[key] = f"*_{_escape_plain(m.group(1))}_*"
        return key

    text = re.sub(r"\*\*\*(.+?)\*\*\*", _bold_italic, text, flags=re.DOTALL)

    # 5. Bold: **text** → *text*
    def _bold(m: re.Match) -> str:
        key = _ph()
        phs[key] = f"*{_escape_plain(m.group(1))}*"
        return key

    text = re.sub(r"\*\*(.+?)\*\*", _bold, text, flags=re.DOTALL)

    # 6. Italic: *text* → _text_
    # No captura bullets (* al inicio de línea con espacio después)
    def _italic(m: re.Match) -> str:
        key = _ph()
        phs[key] = f"_{_escape_plain(m.group(1))}_"
        return key

    text = re.sub(
        r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", _italic, text
    )

    # 7. Strikethrough: ~~text~~ → ~text~
    def _strike(m: re.Match) -> str:
        key = _ph()
        phs[key] = f"~{_escape_plain(m.group(1))}~"
        return key

    text = re.sub(r"~~(.+?)~~", _strike, text, flags=re.DOTALL)

    # 8. Links: [text](url) → [text](url)
    def _link(m: re.Match) -> str:
        key = _ph()
        link_text = _escape_plain(m.group(1))
        url = m.group(2).replace("\\", "\\\\").replace(")", "\\)")
        phs[key] = f"[{link_text}]({url})"
        return key

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link, text)

    # 9. Escapar texto plano y restaurar placeholders
    if phs:
        pattern = re.compile(
            "(" + "|".join(re.escape(k) for k in phs) + ")"
        )
        segments = pattern.split(text)
        return "".join(
            phs[s] if s in phs else _escape_plain(s) for s in segments
        )
    return _escape_plain(text)


def markdown_to_telegram_v2(text: str) -> str:
    """
    Convierte Markdown estándar generado por un LLM a MarkdownV2 de Telegram.

    Soporta:
    - Encabezados (#, ##, ###...) → negrita
    - Separadores horizontales (---) → línea visual
    - Negrita (**text**) → *text*
    - Cursiva (*text*) → _text_
    - Tachado (~~text~~) → ~text~
    - LaTeX ($...$, \\(...\\)) → código inline
    - Bloques de código (```lang...```) → preservados verbatim
    - Código inline (`code`) → preservado verbatim
    - Links [text](url) → preservados con escapes correctos
    - Todo el texto plano con escapes completos de MarkdownV2
    """
    if not text:
        return ""

    # Fase 1: Proteger bloques de código ```...```
    code_blocks: dict[str, str] = {}
    cb_count = [0]

    def _protect_code_block(m: re.Match) -> str:
        lang = (m.group(1) or "").strip()
        code = m.group(2).rstrip("\n")
        key = f"\x01CB{cb_count[0]}\x01"
        cb_count[0] += 1
        prefix = f"```{lang}\n" if lang else "```\n"
        code_blocks[key] = f"{prefix}{code}\n```"
        return key

    text = re.sub(r"```(\w*)\n?([\s\S]*?)```", _protect_code_block, text)

    # Fase 2: Proteger código inline `...`
    inline_codes: dict[str, str] = {}
    ic_count = [0]

    def _protect_inline(m: re.Match) -> str:
        key = f"\x01IC{ic_count[0]}\x01"
        ic_count[0] += 1
        inline_codes[key] = f"`{m.group(1)}`"
        return key

    text = re.sub(r"`([^`\n]+)`", _protect_inline, text)

    # Fase 3: Convertir el texto no-código y restaurar código protegido
    all_protected = {**code_blocks, **inline_codes}
    if all_protected:
        pattern = re.compile(
            "(" + "|".join(re.escape(k) for k in all_protected) + ")"
        )
        segments = pattern.split(text)
        text = "".join(
            all_protected[s] if s in all_protected else _convert_non_code(s)
            for s in segments
        )
    else:
        text = _convert_non_code(text)

    return text


def sanitize_markdown(text: str) -> str:
    """Alias mantenido por compatibilidad. Convierte Markdown a MarkdownV2 de Telegram."""
    return markdown_to_telegram_v2(text)
