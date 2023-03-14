import abc

class TTSInterface:
    @abc.abstractmethod
    def get_tts_audio(self):
        pass