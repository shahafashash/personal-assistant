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
                self._recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = self._recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("5 Seconds Passed")
            return  ## If there was a 5 seconds silcence or unrecognizable sound, the listener will return None
        except sr.RequestError as e:
            print(f"Could not request results: {e}")

        try:
            ## Where does recognize_google comes from?
            ## It was the recognizer who threw the UnkownValueError
            ## The audio threshhold is very low, its enough for the mic to be open for the prgoram to hear anything
            message = self._recognizer.recognize_google(audio)
            print(f"You said: {message}")
            return message
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
