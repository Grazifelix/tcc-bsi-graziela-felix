import json
import ollama
from .base_llm_provider import BaseLLMProvider

class OllamaProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name

    def generate_json(self, prompt: str) -> dict:
        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            format="json"
        )
        return json.loads(response["message"]["content"])