import pytube

class YouTubeAudioDownloader:
    def __init__(self, video_url, dest_path):
        self.video_url = video_url
        self.dest_path = dest_path
    
    def download_audio(self):
        try:
            # Create a YouTube object for the video
            video = pytube.YouTube(self.video_url)

            # Get the audio stream
            audio_stream = video.streams.get_audio_only()

            # Download the audio file to the destination path
            audio_stream.download(output_path=self.dest_path)

            print('Audio download complete.')

        except pytube.exceptions.PytubeError as e:
            print(f'An error occurred: {e}')

# Example usage
video_url = 'https://www.youtube.com/watch?v=-LIIf7E-qFI'
dest_path = './AudioClips'
downloader = YouTubeAudioDownloader(video_url, dest_path)
downloader.download_audio()