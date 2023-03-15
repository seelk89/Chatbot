import os
import time
import uuid
import contextlib

from TextToSpeech.TTSInterface import TTSInterface
from gtts import gTTS
from gtts.tokenizer.pre_processors import abbreviations, end_of_line
with contextlib.redirect_stdout(None):
    from pygame import mixer

from mutagen.mp3 import MP3

class GTTS(TTSInterface):
    def __init__(self, language='en', speed=False):
        self.language = language
        self.speed = speed
        self.audio = None

    def get_tts_audio(self, text):
        # slow=False tells the module that the converted audio should have a high speed
        tts_audio = gTTS(text, lang=self.language, slow=self.speed, pre_processor_funcs = [abbreviations, end_of_line])
        
        self.audio = tts_audio

        ct = f'{uuid.uuid4()}.mp3'
        tts_audio.save(ct)

        self.play_audio(ct)
        
        os.remove(ct)

    def save_tts(self):
        # Should prob open file explorer to select a destination instead.
        self.audio.save(f'{uuid.uuid4()}.mp3')
    
    def play_audio(self, file_path):
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()

        # Wait for the audio to be played
        time.sleep(MP3(file_path).info.length)

        mixer.quit()
