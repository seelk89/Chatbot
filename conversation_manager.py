import keyboard

# Import modules from the same package
from Generator.generatorInterface import GeneratorInterface
from Generator.GPTNeoGenerator import GPTNeoGenerator
from Generator.GPTChatAPI import OpenaiApiDavinci, OpenaiApiGPT3Turbo
from TextToSpeech.TTSInterface import TTSInterface
from TextToSpeech.gTTS import GTTS
from TextToSpeech.pyttsx3TTS import Pyttsx3TTS
from SpeechToText.STTInterface import STTInterface
from SpeechToText.GoogleApi import GoogleAPISTT


class ConversationManager:
    # Manages a conversation between a user and an AI

    def __init__(self, generator: GeneratorInterface, tts: TTSInterface, stt: STTInterface = None):
        # :param generator: an object that generates AI responses
        # :param tts: an object that generates TTS audio
        # :param stt: an object that transcribes speech to text

        self.generator = generator
        self.tts = tts
        self.stt = stt

    def start_conversation(self):
        # Starts a conversation between a user and an AI
        print('Starting loop.')
        while True:
            # Reset the prompt
            prompt = None

            if self.stt is None:
                # For handling input from the terminal, as opposed to STT
                prompt = str(input('User: '))

            # End the conversation if the user presses 'q'
            if self.stt is None and prompt.lower() == 'q':
                break

            if keyboard.is_pressed('ctrl'):
                prompt = self.stt.get_stt_text()

            if prompt is not None:
                generated_text = self.generator.get_generated_text(prompt)
                print(f'Ai: {generated_text}')

                # Generate TTS audio and play it
                self.play_tts_audio(generated_text)

    def play_tts_audio(self, text: str):
        # Generates TTS audio and plays it
        try:
            # Generate TTS audio
            audio = self.tts.get_tts_audio(text)

            # Play TTS audio
            audio.play()
        except Exception as e:
            # Handle TTS audio generation or playback errors
            print(f'Error playing audio: {str(e)}')


if __name__ == '__main__':
    # Initialize objects for the AI generator, TTS engine, and STT engine
    #generator = GPTNeoGenerator()
    #generator = OpenaiApiDavinci()
    generator = OpenaiApiGPT3Turbo()
    #tts = GTTS()
    tts = Pyttsx3TTS()
    stt = GoogleAPISTT()

    # Create a conversation manager and start the conversation
    conversation_manager = ConversationManager(generator, tts, stt)
    conversation_manager.start_conversation()
