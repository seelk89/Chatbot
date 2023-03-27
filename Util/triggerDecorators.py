import logging
import keyboard
import speech_recognition as sr

class TriggerDecorators:
    @staticmethod
    def key_press(keys):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if any(keyboard.is_pressed(key) for key in keys):
                    return func(*args, **kwargs)
            return wrapper
        return decorator

    # For that Alexa / Google assistant feel
    def detect_phrase(keywords):
        def decorator(func):
            def wrapper(*args, **kwargs):
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print('Listening for phrases.')
                    audio = recognizer.listen(source)
                try:
                    recognized_text = recognizer.recognize_google(audio)
                    if any(keyword.lower() in recognized_text.lower() for keyword in keywords):
                        return func(*args, **kwargs)
    
                except sr.RequestError as e:
                    logging.error(f'Speech recognition request error: {e}')
                    return None
                except sr.UnknownValueError as e:
                    logging.error(f'Speech recognition unknown value error: {e}')
                    return None
            return wrapper
        return decorator