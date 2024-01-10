from abc import ABC, abstractmethod
import speech_recognition as sr


class Listener(ABC):
    def __init__(self, energy_threshold: int = 300) -> None:
        """Abstract class for a listener.
        Initialize the recognizer with the given energy threshold.

        Args:
            energy_threshold (int): The energy threshold. Defaults to 300.
        """
        self._recognizer = sr.Recognizer()
        self._recognizer.energy_threshold = energy_threshold

    @property
    def recognizer(self) -> sr.Recognizer:
        """Get the recognizer.

        Returns:
            sr.Recognizer: The recognizer.
        """
        return self._recognizer

    @abstractmethod
    def listen(self) -> str:
        """Listen for a command and return the recognized text.

        Returns:
            str: The recognized text.
        """
        raise NotImplementedError("listen() must be implemented by subclass.")


class BasicListener(Listener):
    def listen(self) -> str:
        """Listen for a command and return the recognized text.

        Returns:
            str: The recognized text or an empty string if nothing was recognized.
        """
        try:
            with sr.Microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = self._recognizer.listen(source, timeout=5)
                # message = self._recognizer.recognize_google(audio)
                message = self._recognizer.recognize_whisper(audio, model="base.en")
                print(f"You said: {message}")
                return message
        except sr.WaitTimeoutError:
            print("5 Seconds Passed")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
            return ""
