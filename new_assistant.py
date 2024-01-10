from typing import List, Optional, Callable
from abc import ABC, abstractmethod
from voices_new.voice import VoiceType, VoiceVolume, Voice, GVoice
from listeners.listener import BasicListener
from sound_effects.effects import SoundEffect
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


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
        self._client = OpenAI()

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
        self._wake_sound = SoundEffect("sound_effects/sounds/wake_sound.wav")
        self._sleep_sound = SoundEffect("sound_effects/sounds/sleep_sound.wav")
        self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a british personal assistant."},
            ],
        )

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
                if self._wake_word in message.lower():
                    return True
        except Exception as e:
            print(e)
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
        should_wait_for_wake_word = True
        while True:
            if should_wait_for_wake_word:
                while not self.listen_to_wake_word():
                    pass
            should_wait_for_wake_word = False
            self._wake_sound.play()
            message = self.listen()
            if not message:
                self._sleep_sound.play()
                should_wait_for_wake_word = True
                continue
            print(message)
            response = self._client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message},
                ],
            )
            self.speak(response.choices[0].text)

            # print("Waiting for wake word...")
            # if self.listen_to_wake_word():
            #     self._wake_sound.play()
            #     print("listening...")
            #     message = self.listen()
            #     if not message:
            #         self._sleep_sound.play()
            #         continue
            #     print(message)
            #     self.speak(message)

            # command = self.parse_command(message)
            # command()


if __name__ == "__main__":
    voice = GVoice(VoiceType.ENGLISH_UNITED_STATES, VoiceVolume.NORMAL)
    listener = BasicListener(energy_threshold=300)
    assistant = BasicAssistant("friday", voice, listener, wake_word="friday")
    assistant.run()
