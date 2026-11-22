from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
        env_file = (".env", "../.env"),
        env_ignore_empty=True,
        extra="ignore",
    )

class DatabaseSettings(BaseSettings):
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_SERVER:str
    POSTGRES_PORT:int
    POSTGRES_DB:str
    @property
    def POSTGRES_URL(self) -> str:
        # postgresql + asyncpg driver  (pip install asyncpg)
        password = quote_plus(self.POSTGRES_PASSWORD)
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{password}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = _base_config


settings = DatabaseSettings()
print(settings.model_dump())


class SecuritySetting(BaseSettings):
    JWT_SECRET: str = "Rishu Shukla"
    JWT_ALGORITHM: str = "HS256"

    model_config = _base_config

db_settings = DatabaseSettings()
Securitysettings = SecuritySetting()