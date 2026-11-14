import pyttsx3
import speech_recognition as sr

class SpeechEngine:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
        except Exception:
            self.engine = None

    def speak(self, text):
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                return recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError:
                return "Speech recognition service error"
