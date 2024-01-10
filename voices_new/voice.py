from typing import List
from abc import ABC, abstractmethod
from enum import Enum
from io import BytesIO
import time
from gtts import gTTS
from pygame import mixer

mixer.pre_init(100_000, -16, 2, 2048)
mixer.init()


class VoiceType(Enum):
    ENGLISH_AUSTRALIA = "com.au"
    ENGLISH_UNITED_KINGDOM = "co.uk"
    ENGLISH_UNITED_STATES = "us"
    ENGLISH_CANADA = "ca"
    ENGLISH_INDIA = "co.in"
    ENGLISH_IRELAND = "ie"
    ENGLISH_SOUTH_AFRICA = "co.za"


class VoiceVolume(Enum):
    LOW = 0.3
    NORMAL = 0.5
    HIGH = 1.0


class Voice(ABC):
    def __init__(self, voice: VoiceType, volume: VoiceVolume) -> None:
        self._voice = voice.value
        self._volume = volume.value
        mixer.music.set_volume(self._volume)

    @property
    def voice(self) -> str:
        """Get the voice.

        Returns:
            str: The voice.
        """
        return self._voice

    @property
    def volume(self) -> float:
        """Get the volume.

        Returns:
            float: The volume.
        """
        return self._volume

    @abstractmethod
    def say(self, text: str | List[str]) -> None:
        """Say text using the voice engine.
        Can be a single sentence or a list of sentences to say.

        Args:
            text (str | List[str]): Text to say.
        """
        raise NotImplementedError("say() must be implemented by subclass.")


class GVoice(Voice):
    def __init__(self, voice: VoiceType, volume: VoiceVolume) -> None:
        super().__init__(voice, volume)
        self.__engine = gTTS
        mixer.music.set_volume(self.volume)

    def __text_to_sound(self, text: str) -> mixer.Sound:
        buffer = BytesIO()
        self.__engine(text=text, lang="en", tld=self._voice).write_to_fp(buffer)
        buffer.seek(0)
        sound = mixer.Sound(buffer)
        buffer.close()
        return sound

    def say(self, text: str | List[str]) -> None:
        sounds = []
        if isinstance(text, str):
            sound = self.__text_to_sound(text)
            sounds.append(sound)
        elif isinstance(text, list):
            for sentence in text:
                sound = self.__text_to_sound(sentence)
                sounds.append(sound)
        else:
            raise TypeError("text must be a string or a list of strings.")

        for sound in sounds:
            length = sound.get_length()
            sound.play()
            time.sleep(length)
