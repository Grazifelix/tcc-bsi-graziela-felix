from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseLLMProvider(ABC):
    
    @abstractmethod
    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """Recebe um prompt e devolve a resposta estruturada em JSON."""
        pass