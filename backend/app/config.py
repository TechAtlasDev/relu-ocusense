from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = "FAKE_TOKEN_FOR_TESTING"
    GEMINI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-3.6-flash"
    PORT: int = 8080
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def effective_gemini_api_key(self) -> str | None:
        return self.GEMINI_API_KEY or self.GOOGLE_API_KEY




settings = Settings()
