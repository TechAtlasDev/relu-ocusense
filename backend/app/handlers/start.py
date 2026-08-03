from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador para el comando /start."""
    user = update.effective_user
    name = user.first_name if user else "usuario"
    if update.message:
        await update.message.reply_text(f"Hola {name}, bienvenido al Bot!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador para el comando /help."""
    if update.message:
        await update.message.reply_text("Comandos disponibles:\n/start - Iniciar bot\n/help - Mostrar ayuda")


def get_start_handlers() -> list[CommandHandler]:
    """Retorna los handlers definidos en este módulo."""
    return [
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
    ]
