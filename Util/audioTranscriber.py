import whisper

# Whisper github: https://github.com/openai/whisper

class AudioTranscriber:
    def __init__(self, model_path, audio_file_path, output_file_path):
        self.model_path = model_path
        self.audio_file_path = audio_file_path
        self.output_file_path = output_file_path
    
    def transcribe_audio(self):
        # Load the model
        model = whisper.load_model(self.model_path)

        # Transcribe the audio file
        result = model.transcribe(self.audio_file_path)
        transcription = result['text']

        # Write the transcription to a text file
        with open(self.output_file_path, 'w') as f:
            f.write(transcription)

        print(f'Transcription saved to {self.output_file_path}.')

# Example usage
model_path = 'Models\\base.en.pt'
file_name = 'I will find YouI will Kill You Taken Movie best scene ever  liam neeson'
audio_file_path = f'./AudioClips/{file_name}.mp4'
output_file_path = f'./Transcribtions/{file_name}.txt'
transcriber = AudioTranscriber(model_path, audio_file_path, output_file_path)
transcriber.transcribe_audio()
