from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=r"E:\AI&ML internship tasks\grad project konecta\Finance use case - Finantial Forecasting\Financial-Forecasting\Project\.env",
        env_file_encoding="utf-8"
    )

settings = Settings()

print("Database URL:", settings.DATABASE_URL)
