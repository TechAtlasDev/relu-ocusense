import logging
from app.core.bot import create_app
from app.config import settings

def main() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=log_level,
    )
    logger = logging.getLogger(__name__)

    # Silenciar logs ruidosos de HTTP de httpx y google_genai si el LOG_LEVEL es superior a DEBUG
    if settings.LOG_LEVEL.upper() != "DEBUG":
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
        logging.getLogger("google_genai").setLevel(logging.WARNING)

    logger.info(f"Iniciando el bot de Telegram (LOG_LEVEL={settings.LOG_LEVEL})...")


    if settings.TELEGRAM_BOT_TOKEN == "FAKE_TOKEN_FOR_TESTING":
        logger.warning(
            "El TELEGRAM_BOT_TOKEN configurado es de prueba. Configura una variable .env real para producción."
        )

    app = create_app()
    app.run_polling()


if __name__ == "__main__":
    main()
