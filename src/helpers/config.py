from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    EMBEDDING_MODEL: str
    GENERATION_MODEL: str
    TOP_K: int = 5
    DATA_PATH: str
    MAX_FILE_SIZE:int
    CHUNK_SIZE:int
    CHUNK_OVERLAP:int
    OLLAMA_BASE_URL: str
    LOCAL_EMBEDDING_MODEL: str
    LOCAL_GENERATION_MODEL: str
    EMBEDDING_MODEL_SIZE: int
    INPUT_DEFAULT_MAX_CHARACTERS: int
    GENERATION_DEFAULT_MAX_TOKENS: int
    GENERATION_DEFAULT_TEMPERATURE: float

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()