from typing import List
from abc import ABC, abstractmethod
from enum import Enum


class Voice(ABC):
    @abstractmethod
    def say(self, text: str | List[str]) -> None:
        """Say text using the voice engine.
        Can be a single sentence or a list of sentences to say.

        Args:
            text (str | List[str]): Text to say.
        """
        raise NotImplementedError("say() must be implemented by subclass.")
