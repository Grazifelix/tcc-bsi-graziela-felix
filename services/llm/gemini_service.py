import json
import os
from google import genai
from google.genai import types
from .base_llm_provider import BaseLLMProvider

class GeminiProvider(BaseLLMProvider):
    def __init__(self, model_name: str = "gemini-3.8-flash"):
        # api_key = os.getenv("GEMINI_API_KEY")
        # if not api_key:
        #     raise ValueError("GEMINI_API_KEY não configurada no ambiente.")
        # self.client = genai.Client(api_key=api_key)
        self.client = genai.Client(api_key="")
        self.model_name = model_name

    def generate_json(self, prompt: str) -> dict:
        response = self.client.interactions.create(
            model=self.model_name,
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                # "schema": Recipe.model_json_schema()
            },
        )
        return json.loads(response.output_text)
