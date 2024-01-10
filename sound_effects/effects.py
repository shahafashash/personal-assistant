import time
from pygame import mixer


class SoundEffect:
    def __init__(self, sound_file: str, cut_off: float = None) -> None:
        self._sound_file = sound_file
        self._sound = mixer.Sound(self._sound_file)
        self._cut_off = cut_off if cut_off else self._sound.get_length()

    @property
    def sound_file(self) -> str:
        """Get the sound file.

        Returns:
            str: The sound file.
        """
        return self._sound_file

    @property
    def cut_off(self) -> float:
        """Get the cut off.

        Returns:
            float: The cut off.
        """
        return self._cut_off

    def play(self) -> None:
        """Play the sound effect.

        Args:
            timeout (float, optional): The timeout in seconds. Defaults to 0.
        """
        self._sound.play()
        time.sleep(self._cut_off)
        self._sound.stop()
