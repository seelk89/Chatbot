import abc

class GeneratorInterface:
    @abc.abstractmethod
    def get_tts_audio(self) -> str:
        pass