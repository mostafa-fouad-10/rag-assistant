import logging

from openai import OpenAI

from src.LLM.LLMInterface import GenerationInterface


class LocalGenerationProvider(GenerationInterface):

    def __init__(
        self,
        api_url: str,
        default_input_max_characters: int = 1024,
        default_generation_max_output_tokens: int = 200,
        default_generation_temperature: float = 0.1
    ):

        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.client = OpenAI(
                api_key="ollama",
                base_url=self.api_url,
                timeout=120.0
            )

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def process_text(self, text: str):
        return text.strip()

    def generate_text(
        self,
        prompt: str,
        chat_history: list = None,
        max_output_tokens: int = None,
        temperature: float = None
    ):

        if not self.client:
            self.logger.error("Ollama client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for Ollama was not set")
            return None

        if chat_history is None:
            chat_history = []

        max_output_tokens = (
            max_output_tokens
            if max_output_tokens is not None
            else self.default_generation_max_output_tokens
        )

        temperature = (
            temperature
            if temperature is not None
            else self.default_generation_temperature
        )

        try:

            chat_history.append(
                self.construct_prompt(
                    prompt=prompt,
                    role="user"
                )
            )
            print(">>> Sending request to Ollama...")
            response = self.client.chat.completions.create(
                model=self.generation_model_id,
                messages=chat_history,
                max_tokens=max_output_tokens,
                temperature=temperature
            )
            print(">>> Ollama response received!")
            if (
                not response
                or not response.choices
                or not response.choices[0].message
            ):
                self.logger.error(
                    "Error while generating text with Ollama"
                )
                return None

            return response.choices[0].message.content

        except Exception:
            self.logger.exception(
                "Error while generating text with Ollama"
            )
            return None

    def construct_prompt(self, prompt: str, role: str):

        return {
            "role": role,
            "content": self.process_text(prompt)
        }