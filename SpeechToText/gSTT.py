import logging
import speech_recognition as sr

from SpeechToText.STTInterface import STTInterface

class GSTT(STTInterface):
    # A speech-to-text implementation that uses the Google Speech Recognition API
    def __init__(self, timeout=5):
        # Initializes the recognizer object
        self.recognizer = sr.Recognizer()
        self.timeout = timeout

    def get_stt_text(self) -> str:
        # Listens to the microphone and returns the recognized text as a string
        # Returns None if an error occurs.
        try:
            with sr.Microphone() as source:
                print('Recording.')
                audio = self.recognizer.listen(source, timeout=self.timeout)
                text = self.recognizer.recognize_google(audio)
                print(f'Results: {text}')

                return text

        except sr.RequestError as e:
            logging.error(f'Speech recognition request error: {e}')
            return None
        except sr.UnknownValueError as e:
            logging.error(f'Speech recognition unknown value error: {e}')
            return None
