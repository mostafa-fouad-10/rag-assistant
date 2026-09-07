from src.services.search_service import SearchService
from src.LLM.LLMFactory import LLMFactory
from src.LLM.LLMEnums import LLMProvider
from src.helpers.config import get_settings
from src.helpers.prompt import build_rag_prompt


class RAGService:

    def __init__(self):

        self.search_service = SearchService()

        config = get_settings()

        self.generation_provider = LLMFactory.create_generation_provider(
            provider=LLMProvider.LOCAL.value,
            api_url=config.OLLAMA_BASE_URL
        )

        self.generation_provider.set_generation_model(
            config.LOCAL_GENERATION_MODEL
        )

    def answer(
        self,
        query: str,
        file_id: str
    ):

        results = self.search_service.search_by_vector(
            collection_name="documents",
            query=query,
            limit=5,
            file_id=file_id
        )

        if not results:
            return "I couldn't find relevant information in the document."

        context = "\n\n".join(
            result.text
            for result in results
        )

        prompt = build_rag_prompt(
            context=context,
            query=query
        )

        answer = self.generation_provider.generate_text(
            prompt=prompt
        )

        if answer is None:
            raise RuntimeError(
                "Failed to generate answer from Ollama."
            )

        return answer