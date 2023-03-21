import speech_recognition as sr
import logging

from SpeechToText.STTInterface import STTInterface

# This broke somehow, at some point, and i have no idea why.
class GoogleAPISTT(STTInterface):
    # A speech-to-text implementation that uses the Google Speech Recognition API.
    def __init__(self):
        # Initializes the recognizer object.
        self.recognizer = sr.Recognizer()

    def get_stt_text(self) -> str:
        # Listens to the microphone and returns the recognized text as a string.
        # Returns None if an error occurs.
        try:
            with sr.Microphone() as source:
                print('Recording.')
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                print(f'Results: {text}')

                return text

        except sr.RequestError as e:
            logging.error(f'Speech recognition request error: {e}')
            return None
        except sr.UnknownValueError as e:
            logging.error(f'Speech recognition unknown value error: {e}')
            return None
