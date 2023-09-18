from typing import List
from abc import ABC, abstractmethod
import speech_recognition as sr
from voices.basic import Voice
from voices.gtts_voices import GVoice
from voices.pyttsx3_voices import PyttsxVoice

# import pywhatkit
import os
from dotenv import load_dotenv
import openai

OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY


class Assistant(ABC):
    def __init__(self, name: str, owner: str, voice=Voice) -> None:
        self._recognizer = sr.Recognizer()
        self._listener = sr.Microphone()
        self._voice = voice
        self._name = name.title()
        self._owner = owner.title()

    def speak(self, text: str | List[str]) -> None:
        """Speak the text.

        Args:
            text (str | List[str]): The text to speak.
        """
        self._voice.say(text)

    def listen(self) -> str:
        """Listen for a command.

        Returns:
            str: The command.
        """
        raise NotImplementedError("listen() must be implemented by subclass.")
