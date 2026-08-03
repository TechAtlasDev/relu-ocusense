from telegram.ext import Application
from app.config import settings
from app.handlers.start import get_start_handlers
from app.handlers.general import get_general_handlers


def create_app() -> Application:
    """Construye y ensambla la aplicación del bot con sus handlers."""
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Registro modular de handlers
    handlers = [
        *get_start_handlers(),
        *get_general_handlers(),
    ]

    for handler in handlers:
        application.add_handler(handler)

    return application
