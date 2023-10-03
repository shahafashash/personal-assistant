from typing import List
from enum import Enum
from io import BytesIO
import time
from gtts import gTTS
from pygame import mixer
from .basic import Voice

# mixer.pre_init(44100, -16, 2, 2048)
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


class GVoice(Voice):
    def __init__(
        self,
        volume: VoiceVolume = VoiceVolume.NORMAL,
        voice: VoiceType = VoiceType.ENGLISH_UNITED_STATES,
    ) -> None:
        self._voice = voice.value
        self.__engine = gTTS
        self._volume = volume.value
        mixer.music.set_volume(self._volume)

    @property
    def voice(self) -> VoiceType:
        """Get the voice.

        Returns:
            VoiceType: The voice.
        """
        return self._voice

    @voice.setter
    def voice(self, voice: VoiceType) -> None:
        """Set the voice.

        Args:
            voice (VoiceType): The voice.
        """
        self._voice = voice

    @property
    def volume(self) -> VoiceVolume:
        """Get the volume.

        Returns:
            VoiceVolume: The volume.
        """
        return self._volume

    @volume.setter
    def volume(self, volume: VoiceVolume) -> None:
        """Set the volume.

        Args:
            volume (VoiceVolume): The volume.
        """
        self._volume = volume.value
        mixer.music.set_volume(self._volume)

    def say(self, text: str | List[str]) -> None:
        """Say text using the voice engine.
        Can be a single sentence or a list of sentences to say.

        Args:
            text (str | List[str]): Text to say.
        """
        sounds = []
        if isinstance(text, str):
            buffer = BytesIO()
            self.__engine(text=text, lang="en", tld=self._voice).write_to_fp(buffer)
            buffer.seek(0)
            sound = mixer.Sound(buffer)
            sounds.append(sound)
            buffer.close()
        elif isinstance(text, list):
            for sentence in text:
                buffer = BytesIO()
                self.__engine(text=sentence, lang="en", tld=self._voice).write_to_fp(
                    buffer
                )
                buffer.seek(0)
                sound = mixer.Sound(buffer)
                sounds.append(sound)
                buffer.close()

        for sound in sounds:
            length = sound.get_length()
            sound.play()
            time.sleep(length)
