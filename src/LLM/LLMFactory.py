from src.LLM.LLMEnums import LLMProvider

from src.LLM.providers.local.LocalEmbeddingProvider import (
    LocalEmbeddingProvider
)
from src.LLM.providers.local.LocalGenerationProvider import (
    LocalGenerationProvider
)


class LLMFactory:

    @staticmethod
    def create_embedding_provider(
        provider: str
    ):

        if provider == LLMProvider.LOCAL.value:
            return LocalEmbeddingProvider()

        raise ValueError(
            f"Unsupported embedding provider: {provider}"
        )

    @staticmethod
    def create_generation_provider(
        provider: str,
        api_url: str,
        input_max_characters: int = 1024,
        generation_max_tokens: int = 200,
        generation_temperature: float = 0.1
    ):

        if provider == LLMProvider.LOCAL.value:
            return LocalGenerationProvider(
                api_url=api_url,
                default_input_max_characters=input_max_characters,
                default_generation_max_output_tokens=generation_max_tokens,
                default_generation_temperature=generation_temperature
            )

        raise ValueError(
            f"Unsupported generation provider: {provider}"
        )