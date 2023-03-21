import abc

class STTInterface:
    @abc.abstractmethod
    def get_stt_text(self) -> str:
        pass