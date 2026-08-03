import logging
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI, Request, Response, status
from telegram import Update
from telegram.ext import Application

from app.config import settings
from app.core.bot import create_app

# Configuración de Logging
log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=log_level,
)
logger = logging.getLogger(__name__)

if settings.LOG_LEVEL.upper() != "DEBUG":
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("google_genai").setLevel(logging.WARNING)

# Instancia global del bot de Telegram
telegram_app: Application = create_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida del bot de Telegram y la API FastAPI."""
    logger.info("Inicializando aplicación de Telegram...")
    await telegram_app.initialize()
    await telegram_app.start()

    if settings.USE_WEBHOOK and settings.WEBHOOK_URL:
        full_webhook_url = f"{settings.WEBHOOK_URL.rstrip('/')}{settings.WEBHOOK_PATH}"
        logger.info(f"Configurando Webhook de Telegram en: {full_webhook_url}")
        await telegram_app.bot.set_webhook(
            url=full_webhook_url,
            secret_token=settings.WEBHOOK_SECRET_TOKEN,
        )
    else:
        logger.info("Modo Webhook desactivado o WEBHOOK_URL no configurado.")

    yield

    logger.info("Deteniendo aplicación de Telegram...")
    if settings.USE_WEBHOOK and settings.WEBHOOK_URL:
        try:
            await telegram_app.bot.delete_webhook()
        except Exception as exc:
            logger.warning(f"No se pudo eliminar el webhook: {exc}")
    await telegram_app.stop()
    await telegram_app.shutdown()


app = FastAPI(
    title="ReLU Telegram Bot Backend",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Endpoint de comprobación de salud para Cloud Run."""
    return {"status": "ok", "service": "relu-backend"}


@app.post(settings.WEBHOOK_PATH)
async def telegram_webhook(request: Request) -> Response:
    """Endpoint receptor de Updates de Telegram."""
    if settings.WEBHOOK_SECRET_TOKEN:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret != settings.WEBHOOK_SECRET_TOKEN:
            logger.warning("Token de secreto inválido en petición de webhook.")
            return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)
        # Procesar en segundo plano para responder 200 OK a Telegram inmediatamente
        import asyncio
        asyncio.create_task(telegram_app.process_update(update))
        return Response(status_code=status.HTTP_200_OK)
    except Exception as exc:
        logger.exception("Error procesando actualización de Webhook: %s", exc)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def main() -> None:
    import uvicorn

    logger.info(f"Iniciando servidor Uvicorn en el puerto {settings.PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)


if __name__ == "__main__":
    main()
