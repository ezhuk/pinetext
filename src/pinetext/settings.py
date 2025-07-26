from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Pinecone(BaseModel):
    api_key: str | None = None
    assistant: str | None = None
    model: str | None = None


class Settings(BaseSettings):
    pinecone: Pinecone = Pinecone()
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
