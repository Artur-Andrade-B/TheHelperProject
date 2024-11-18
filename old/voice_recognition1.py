# voice_recognition.py
import speech_recognition as sr

class VoiceRecognizer:
    def __init__(self, language='pt-BR'):
        self.recognizer = sr.Recognizer()
        self.language = language

    def listen(self):
        # Listen to the microphone for a voice command
        with sr.Microphone() as source:
            print("Listening for command...")
            audio = self.recognizer.listen(source)
            try:
                # Recognize speech using Google Speech Recognition
                print("Recognizing command...")
                command = self.recognizer.recognize_google(audio, language=self.language)
                print(f"Command recognized: {command}")
                return command.lower()  # Return the recognized command in lowercase
            except sr.UnknownValueError:
                print("Sorry, I could not understand the command.")
                return None
            except sr.RequestError:
                print("Sorry, there was an issue with the speech recognition service.")
                return None
