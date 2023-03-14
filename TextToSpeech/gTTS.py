import os
import time
import mutagen

from TextToSpeech.TTSInterface import TTSInterface
from datetime import date
from gtts import gTTS
from gtts.tokenizer.pre_processors import abbreviations, end_of_line
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

        ct = f'{date.today()}.mp3'
        tts_audio.save(ct)

        mixer.init()
        mixer.music.load(ct)
        mixer.music.play()

        # Wait for the audio to be played
        # This should be done in a seperate thread
        time.sleep(MP3(ct).info.length)

        mixer.quit()

        os.remove(ct)

    def save_tts(self):
        # Should prob open file explorer to select a destination instead.
        self.audio.save(f'{date.today()}.mp3')
