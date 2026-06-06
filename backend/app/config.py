from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "flymetrics_project"
    database_url: str | None = None

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "http://localhost:5500,"
        "http://127.0.0.1:5500,"
        "http://localhost:8001,"
        "http://127.0.0.1:8001,"
        "null"
    )

    secret_key: str = "cambia-esta-clave-en-produccion"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url

        password = quote_plus(self.db_password)
        return (
            f"mysql+pymysql://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
