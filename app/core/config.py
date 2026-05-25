from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    # Field(..., ...) satisfies the type checker while telling Pydantic it's required
    PROJECT_NAME: str = Field(...)
    VERSION: str = Field(...)

    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_SERVER: str = Field(...)
    POSTGRES_PORT: int = Field(...)
    POSTGRES_DB: str = Field(...)

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()