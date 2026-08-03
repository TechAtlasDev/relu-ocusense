import asyncio
import logging
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes, MessageHandler, filters
from app.services.llm import llm_service

logger = logging.getLogger(__name__)



from app.utils.formatter import sanitize_markdown


async def handle_llm_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador que procesa mensajes asignando memoria a cada usuario según su chat_id de Telegram."""
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    chat_id = update.effective_chat.id if update.effective_chat else None

    if not chat_id:
        return

    thread_id = str(chat_id)

    # Enviar acción 'typing' inicial
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Mensaje inicial temporal
    sent_message = await update.message.reply_text("*Pensando...*", parse_mode=ParseMode.MARKDOWN)

    response_message = None
    last_update_text = ""
    partial_text = ""
    chunk_counter = 0

    try:
        tool_used_name = None
        async for item in llm_service.generate_response_stream(user_text, thread_id=thread_id):
            # Si se notifica el uso de una herramienta
            if isinstance(item, dict) and item.get("type") == "tool_used":
                tool_used_name = item.get("tool_name")
                tool_msg = f"⚙️ *ReLU utilizó la herramienta:* `{tool_used_name}`"
                try:
                    # Transformamos el mensaje inicial "Pensando..." en la notificación de la herramienta utilizada
                    await sent_message.edit_text(tool_msg, parse_mode=ParseMode.MARKDOWN)
                except Exception:
                    pass
                continue

            # Si recibimos el texto explicativo generado por la IA
            if isinstance(item, str):
                partial_text = item
                
                # Si se utilizó una herramienta, la respuesta de la IA debe ir en un mensaje nuevo después de la notificación
                if tool_used_name and not response_message:
                    try:
                        response_message = await update.message.reply_text("*Generando respuesta...*", parse_mode=ParseMode.MARKDOWN)
                    except Exception:
                        response_message = sent_message
                elif not response_message:
                    response_message = sent_message

                chunk_counter += 1
                if chunk_counter % 5 == 0:
                    formatted = sanitize_markdown(partial_text)
                    if formatted != last_update_text:
                        try:
                            await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
                            await response_message.edit_text(formatted, parse_mode=ParseMode.MARKDOWN)
                            last_update_text = formatted
                        except Exception:
                            pass

        target_msg = response_message or sent_message
        final_formatted = sanitize_markdown(partial_text)
        if final_formatted and final_formatted != last_update_text:
            try:
                await target_msg.edit_text(final_formatted, parse_mode=ParseMode.MARKDOWN)
            except Exception:
                try:
                    # Fallback si Telegram rechaza sintaxis de Markdown compleja
                    await target_msg.edit_text(partial_text)
                except Exception:
                    pass

    except Exception as exc:
        logger.exception("Error al procesar el mensaje con Gemini/Telegram: %s", exc)
        if last_update_text:
            try:
                await sent_message.edit_text(last_update_text)
            except Exception:
                pass
        else:
            try:
                await sent_message.edit_text("Ocurrió un error al procesar tu solicitud.")
            except Exception:
                pass





def get_general_handlers() -> list:
    """Retorna handlers generales o por defecto."""
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_llm_chat),
    ]
