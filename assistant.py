from typing import List, Callable
from abc import ABC, abstractmethod
import string
import random
import speech_recognition as sr
from voices.basic import Voice
from voices.gtts_voices import GVoice
from voices.gtts_voices import VoiceType as GVoiceType
from voices.gtts_voices import VoiceVolume as GVoiceVolume
from voices.pyttsx3_voices import PyttsxVoice
from voices.pyttsx3_voices import VoiceType as PyttsxVoiceType
from voices.pyttsx3_voices import VoiceVolume as PyttsxVoiceVolume
from voices.pyttsx3_voices import VoiceRate as PyttsxVoiceRate

# import pywhatkit
import os
from dotenv import load_dotenv
import openai

load_dotenv()

# OPENAI_KEY = os.getenv("OPENAI_KEY")
# openai.api_key = OPENAI_KEY


class Assistant(ABC):
    def __init__(
        self, name: str, owner: str, voice=Voice, wake_word: str = None
    ) -> None:
        self._recognizer = sr.Recognizer()
        self._voice = voice
        self._name = name.title()
        self._owner = owner.title()
        self._wake_word = wake_word if wake_word else self._name.lower()

    def get_greeting(self) -> str:
        # a list of greetings to randomly choose from. Feel free to use owner's name
        greetings = [
            f"Hello, {self._owner}.",
            f"Hi, {self._owner}.",
            f"Hey, {self._owner}.",
            f"What's up, {self._owner}.",
            f"How's it going, {self._owner}.",
            f"Talk to me, {self._owner}.",
            f"Good day, {self._owner}.",
            f"What can I do for you, {self._owner}.",
            f"Good to see you, {self._owner}.",
            f"Yes, {self._owner}?",
            "Yo",
            "Hey",
            "Hi",
            "Hello",
            "What's up",
            "How's it going",
        ]

        follow_ups = [
            "How can I help you?",
            "What can I do for you?",
            "What would you like me to do?",
            "What do you need?",
            "What can I do for you today?",
            "How can I be of service?",
        ]

        greeting = random.choice(greetings)
        follow_up = random.choice(follow_ups)
        add_follow_up = random.randint(0, 1)
        if add_follow_up:
            return f"{greeting} {follow_up}"
        else:
            return greeting

    def get_action_received_acknowledgement(self) -> str:
        # a list of acknowledgements to randomly choose from. Feel free to use owner's name
        acknowledgements = [
            f"Right away, {self._owner}.",
            f"Sure thing, {self._owner}.",
            f"Of course, {self._owner}.",
            f"Okay, {self._owner}.",
            f"Alright, {self._owner}.",
            f"Got it, {self._owner}.",
            f"Will do, {self._owner}.",
            f"Consider it done, {self._owner}.",
            f"Consider it handled, {self._owner}.",
            f"Gladly, {self._owner}.",
            f"Absolutely, {self._owner}.",
            f"Sure, {self._owner}.",
            "Okay",
            "Alright",
            "Got it",
            "Will do",
            "Consider it done",
            "Consider it handled",
            "Gladly",
            "Absolutely",
            "Sure",
        ]

        acknowledgement = random.choice(acknowledgements)
        return acknowledgement

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
        while True:
            try:
                with sr.Microphone() as source:
                    self._recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self._recognizer.listen(source)
                    message = self._recognizer.recognize_google(audio)
                    print(f"You said: {message}")
                    return message
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except sr.UnknownValueError:
                print("Sorry, I did not get that.")

    def listen_for_wake_word(self) -> bool:
        message = self.listen()
        # clear the message of punctuation and capitalization
        message = message.translate(str.maketrans("", "", string.punctuation))
        if self._wake_word.lower() in message.lower():
            return True
        return False

    def listen_for_action(self) -> str:
        message = self.listen()
        return self.parse_request(message)

    def get_action(self, action: str) -> Callable:
        """Get the action function.

        Args:
            action (str): The action to get the function for.

        Returns:
            Callable: The function.
        """
        # getting all the methods of the class that start with "action_"
        methods = [
            method
            for method in dir(self)
            if callable(getattr(self, method)) and method.startswith("action_")
        ]
        if action in methods:
            return getattr(self, action)
        else:
            raise AttributeError(f"Action {action} not found.")

    @abstractmethod
    def parse_request(self, request: str) -> str:
        """Parse the request.

        Args:
            request (str): The request to parse.

        Returns:
            str: The parsed request.
        """
        pass

    def run(self) -> None:
        """Run the assistant."""
        wait_for_wake_word = True
        while True:
            print("listening...")
            if wait_for_wake_word:
                if self.listen_for_wake_word():
                    greeting = self.get_greeting()
                    self.speak(greeting)
                    wait_for_wake_word = False
            else:
                action = self.listen_for_action()
                print(f"Executing {action}")
                acknowledgement = self.get_action_received_acknowledgement()
                self.speak(acknowledgement)
                # self.get_action(action)()
                wait_for_wake_word = True


class Friday(Assistant):
    def __init__(self) -> None:
        voice = GVoice(voice=GVoiceType.ENGLISH_AUSTRALIA, volume=GVoiceVolume.NORMAL)
        name = "friday"
        owner = "boss"
        super().__init__(name, owner, voice, wake_word="hey friday")

    def parse_request(self, request: str) -> str:
        return request


class Hazel(Assistant):
    def __init__(self) -> None:
        voice = PyttsxVoice(
            voice=PyttsxVoiceType.HAZEL,
            volume=PyttsxVoiceVolume.HIGH,
            rate=PyttsxVoiceRate.NORMAL,
        )
        name = "jarvis"
        owner = "boss"
        super().__init__(name, owner, voice, wake_word="hey hazel")

    def parse_request(self, request: str) -> str:
        return request


if __name__ == "__main__":
    # friday = Friday()
    # friday.run()

    hazel = Hazel()
    hazel.run()

    # for device in sr.Microphone.list_microphone_names():
    #     print(device)
    # devices = sr.Microphone.list_microphone_names()
    # razer_mic = devices.index("Microphone (Razer BlackShark V2 Pro)")
    # print(razer_mic)
    # recognizer = sr.Recognizer()
    # with sr.Microphone(device_index=razer_mic) as source:
    #     recognizer.adjust_for_ambient_noise(source, duration=1)
    #     print(source.device_index)
    #     audio = recognizer.listen(source, phrase_time_limit=5)
    #     message = recognizer.recognize_google(audio)
    #     print(f"You said: {message}")
