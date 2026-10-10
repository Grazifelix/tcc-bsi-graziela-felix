import os
from .base_llm_provider import BaseLLMProvider
from .ollama_service import OllamaProvider
from .gemini_service import GeminiProvider

def get_llm_provider() -> BaseLLMProvider:
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider == "gemini":
        model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        return GeminiProvider(model_name=model)
    elif provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
        return OllamaProvider(model_name=model)
    else:
        raise ValueError(f"Provedor LLM desconhecido: {provider}")