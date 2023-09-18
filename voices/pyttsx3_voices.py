from typing import List
from enum import Enum
import pyttsx3
from .basic import Voice


class VoiceRate(Enum):
    SLOW = 100
    NORMAL = 150
    FAST = 300


class VoiceVolume(Enum):
    LOW = 0.3
    NORMAL = 0.5
    HIGH = 1.0


class VoiceType(Enum):
    DAVID = 0
    JAMES = 1
    MATILDA = 2
    LINDA = 3
    RICHARD = 4
    GEORGE = 5
    SUSAN = 6
    EVA = 7
    MARK = 8
    HAZEL = 9
    CATHERINE = 10
    ZIRA = 11


class PyttsxVoice(Voice):
    def __init__(
        self,
        rate: VoiceRate = VoiceRate.NORMAL,
        volume: VoiceVolume = VoiceVolume.NORMAL,
        voice: VoiceType = VoiceType.DAVID,
    ) -> None:
        self.__engine = pyttsx3.init()
        self.__voices = self.__engine.getProperty("voices")
        self._rate = rate.value
        self._volume = volume.value
        self._voice = voice.value
        self.__engine.setProperty("rate", self._rate)
        self.__engine.setProperty("volume", self._volume)
        self.__engine.setProperty("voice", self.__voices[self._voice].id)

    @property
    def rate(self) -> VoiceRate:
        """Get the voice rate.

        Returns:
            VoiceRate: The voice rate.
        """
        for rate in VoiceRate:
            if rate.value == self._rate:
                return rate

    @rate.setter
    def rate(self, rate: VoiceRate) -> None:
        """Set the voice rate.

        Args:
            rate (VoiceRate): The voice rate.
        """
        self._rate = rate.value
        self.__engine.setProperty("rate", self._rate)

    @property
    def volume(self) -> VoiceVolume:
        """Get the voice volume.

        Returns:
            VoiceVolume: The voice volume.
        """
        for volume in VoiceVolume:
            if volume.value == self._volume:
                return volume

    @volume.setter
    def volume(self, volume: VoiceVolume) -> None:
        """Set the voice volume.

        Args:
            volume (VoiceVolume): The voice volume.
        """
        self._volume = volume.value
        self.__engine.setProperty("volume", self._volume)

    @property
    def voice(self) -> VoiceType:
        """Get the voice type.

        Returns:
            VoiceType: The voice type.
        """
        for voice in VoiceType:
            if voice.value == self._voice:
                return voice

    @voice.setter
    def voice(self, voice: VoiceType) -> None:
        """Set the voice type.

        Args:
            voice (VoiceType): The voice type.
        """
        self._voice = voice.value
        self.__engine.setProperty("voice", self.__voices[self._voice].id)

    def say(self, text: str | List[str]) -> None:
        """Say text using the voice engine.
        Can be a single sentence or a list of sentences to say.

        Args:
            text (str | List[str]): Text to say.
        """
        if isinstance(text, str):
            self.__engine.say(text)
        else:
            for line in text:
                self.__engine.say(line)
        self.__engine.runAndWait()
