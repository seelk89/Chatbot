import keyboard
import multiprocessing

from Generator.generatorInterface import GeneratorInterface
from Generator.GPTNeoGenerator import GPTNeoGenerator
from Generator.GPTChatAPI import OpenaiApiDavinci, OpenaiApiGPT3Turbo
from TextToSpeech.TTSInterface import TTSInterface
from TextToSpeech.gTTS import GTTS
from TextToSpeech.pyttsx3TTS import Pyttsx3TTS
from SpeechToText.STTInterface import STTInterface
from SpeechToText.GoogleApi import GoogleAPISTT

class Main:
    def __init__(self, generator: GeneratorInterface, tts: TTSInterface, stt: STTInterface = None):
        self.generator = generator
        self.tts = tts
        self.stt = stt

    def main(self):
        print('Starting loop.')
        while True:
            # Reset the prompt
            prompt = None

            if self.stt == None:
                # For handling input from the terminal, as opposed to STT
                prompt = str(input('User: '))

            # End the conversation if the user presses 'q'
            if self.stt == None and prompt.lower() == 'q':
                break

            if keyboard.is_pressed('ctrl'):
                prompt = self.stt.get_stt_text()
            
            if prompt != None:
                generated_text = self.generator.get_generated_text(prompt)
                print(f'Ai: {generated_text}')
                p = multiprocessing.Process(target=self.tts.get_tts_audio, args=(generated_text,))
                p.start()

if __name__ == '__main__':
    #generator = GPTNeoGenerator()
    #generator = OpenaiApiDavinci()
    generator = OpenaiApiGPT3Turbo()
    #tts = GTTS()
    tts = Pyttsx3TTS()
    stt = GoogleAPISTT()

    main = Main(generator, tts, stt)
    main.main()
