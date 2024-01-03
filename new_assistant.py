from typing import List, Optional, Callable
from abc import ABC, abstractmethod
import time
from voices_new.voice import VoiceType, VoiceVolume, Voice, GVoice
from listeners.listener import BasicListener


class Assistant(ABC):
    def __init__(
        self,
        name: str,
        voice: Voice,
        listener: BasicListener,
        wake_word: Optional[str] = None,
    ) -> None:
        self._name = name.title()
        self._voice = voice
        self._listener = listener
        self._wake_word = wake_word if wake_word else self._name.lower()

    @abstractmethod
    def speak(self, text: str | List[str]) -> None:
        """Speak text using the voice engine.
        Can be a single sentence or a list of sentences to speak.

        Args:
            text (str | List[str]): Text to speak.
        """
        raise NotImplementedError("speak() must be implemented by subclass.")

    @abstractmethod
    def listen(self) -> str:
        """Listen to the user and return the text.

        Returns:
            str: The text.
        """
        raise NotImplementedError("listen() must be implemented by subclass.")

    @abstractmethod
    def listen_to_wake_word(self) -> bool:
        """Listen to the user and return the text.

        Returns:
            bool: Whether the wake word was detected.
        """
        raise NotImplementedError(
            "listen_to_wake_word() must be implemented by subclass."
        )

    @abstractmethod
    def parse_command(self, command: str) -> Callable:
        """Parse the command and execute it.

        Args:
            command (str): The command to parse.
        """
        raise NotImplementedError("parse_command() must be implemented by subclass.")

    @abstractmethod
    def run(self) -> None:
        """Run the assistant."""
        raise NotImplementedError("run() must be implemented by subclass.")


class BasicAssistant(Assistant):
    def __init__(
        self,
        name: str,
        voice: Voice,
        listener: BasicListener,
        wake_word: Optional[str] = None,
    ) -> None:
        super().__init__(name, voice, listener, wake_word)

    def speak(self, text: str | List[str]) -> None:
        """Speak text using the voice engine.
        Can be a single sentence or a list of sentences to speak.

        Args:
            text (str | List[str]): Text to speak.
        """
        self._voice.say(text)

    def listen(self) -> str:
        """Listen to the user and return the text.

        Returns:
            str: The text.
        """
        return self._listener.listen()

    def listen_to_wake_word(self) -> bool:
        """Listen to the user and return the text.

        Returns:
            str: The text.
        """
        try:
            while True:
                message = self.listen()
                if type(message) is not str:
                    break
                if self._wake_word in message.lower():
                    return True
        except:
            return False

    def parse_command(self, command: str) -> Callable:
        """Parse the command and execute it.

        Args:
            command (str): The command to parse.
        """
        pass

    def run(self) -> None:
        """Run the assistant."""
        print("listening...")
        while True:
            print("Waiting for wake word...")
            if self.listen_to_wake_word():
                self.speak("Hello, how can I help you?")
                sentance = []
                while True:
                    message = self.listen()
                    if type(message) is not str:
                        break
                    sentance.append(message)
                print(sentance)
                self.speak(sentance)

            # command = self.parse_command(message)
            # command()


if __name__ == "__main__":
    voice = GVoice(VoiceType.ENGLISH_UNITED_STATES, VoiceVolume.NORMAL)
    listener = BasicListener()
    assistant = BasicAssistant("friday", voice, listener, wake_word="friday")
    assistant.run()
