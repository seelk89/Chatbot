import speech_recognition as sr

from SpeechToText.STTInterface import STTInterface

# Whisper github: https://github.com/openai/whisper

class WhisperSTT(STTInterface):
    def __init__(self, model_path='./Models/base.en.pt', timeout=5):
        # Initializes the recognizer object.
        self.recognizer = sr.Recognizer()
        self.model_path = model_path
        self.timeout = timeout
    
    def get_stt_text(self) -> str:
        # Performs speech-to-text using the Whisper model and returns the recognized text.
        # Returns None if an error occurs.
        with sr.Microphone() as source:
            print('Recording.')
            audio = self.recognizer.listen(source, timeout=self.timeout)
            try:
                text = self.recognizer.recognize_whisper(audio, model=self.model_path)
                print(f'Results: {text}')
                return text

            except sr.UnknownValueError:
                print('Unable to recognize speech.')
                return None
            except sr.RequestError as e:
                print(f'Request error: {e}')
                return None