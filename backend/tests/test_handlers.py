import pytest
from unittest.mock import AsyncMock, MagicMock
from app.handlers.start import start_command, help_command


@pytest.mark.asyncio
async def test_start_command():
    update = MagicMock()
    update.effective_user.first_name = "Juan"
    update.message = AsyncMock()

    context = MagicMock()

    await start_command(update, context)

    update.message.reply_text.assert_called_once_with("Hola Juan, bienvenido al Bot!")


@pytest.mark.asyncio
async def test_help_command():
    update = MagicMock()
    update.message = AsyncMock()

    context = MagicMock()

    await help_command(update, context)

    update.message.reply_text.assert_called_once_with(
        "Comandos disponibles:\n/start - Iniciar bot\n/help - Mostrar ayuda"
    )


@pytest.mark.asyncio
async def test_handle_llm_chat():
    from app.handlers.general import handle_llm_chat

    update = MagicMock()
    update.effective_chat.id = 12345
    update.message = AsyncMock()
    update.message.text = "Hola bot"

    sent_message = AsyncMock()
    update.message.reply_text.return_value = sent_message

    context = MagicMock()
    context.bot.send_chat_action = AsyncMock()

    await handle_llm_chat(update, context)

    # Verificar que se envió la acción de escribir y la respuesta inicial
    context.bot.send_chat_action.assert_called_with(chat_id=12345, action="typing")
    update.message.reply_text.assert_called_once()
    assert sent_message.edit_text.called

