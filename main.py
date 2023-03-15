import multiprocessing

from Generator.generatorInterface import GeneratorInterface
from Generator.GPTNeoGenerator import GPTNeoGenerator
from TextToSpeech.TTSInterface import TTSInterface
from TextToSpeech.gTTS import GTTS

class Main:
    def __init__(self, generator: GeneratorInterface, tts: TTSInterface):
        self.generator = generator
        self.tts = tts

    def main(self):
        while True:
            prompt = str(input('User: '))

            # End the conversation if the user presses 'q'
            if prompt.lower() == 'q':
                break
            
            generated_text = self.generator.get_generated_text(prompt)
            print(f'Ai: {generated_text}')
            p = multiprocessing.Process(target=self.tts.get_tts_audio, args=(generated_text,))
            p.start()

if __name__ == "__main__":
    generator = GPTNeoGenerator()
    tts = GTTS()

    main = Main(generator, tts)
    main.main()
