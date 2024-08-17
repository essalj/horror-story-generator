

from moviepy.editor import VideoFileClip

def extract_audio(mp4_file, mp3_file):
    video = VideoFileClip(mp4_file)
    audio = video.audio
    audio.write_audiofile(mp3_file)
    audio.close()
    video.close()

# Usage
input_mp4 = r"C:\my\__youtube\videos\2024-07-20_2243_Truly Scary Ouija Stories_compilation\Truly Scary Ouija Stories - rain.mp4"
output_mp3 = r"C:\my\__youtube\videos\2024-07-20_2243_Truly Scary Ouija Stories_compilation\Truly Scary Ouija Stories - rain.mp3"

extract_audio(input_mp4, output_mp3)
print(f"Audio extracted and saved as {output_mp3}")


