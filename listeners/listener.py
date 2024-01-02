from abc import ABC, abstractmethod
import speech_recognition as sr


class Listener(ABC):
    def __init__(self) -> None:
        self._recognizer = sr.Recognizer()

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
            str: The recognized text.

        Raises:
            sr.RequestError: If the request fails.
            sr.UnknownValueError: If the value is unknown.
        """
        try:
            with sr.Microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self._recognizer.listen(source)
                message = self._recognizer.recognize_google(audio)
                print(f"You said: {message}")
                return message
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
