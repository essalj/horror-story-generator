

from pydub import AudioSegment, effects
import os

def normalize_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    normalized_audio = effects.normalize(audio)
    normalized_audio.export(output_path, format="mp3")

directory = "C:\\my\\__youtube\\videos\\horror_music"
normalized_directory = "C:\\my\\__youtube\\videos\\horror_music\\eqalized"

if not os.path.exists(normalized_directory):
    os.makedirs(normalized_directory)

for filename in os.listdir(directory):
    if filename.endswith(".mp3"):
        input_path = os.path.join(directory, filename)
        output_path = os.path.join(normalized_directory, filename)
        normalize_audio(input_path, output_path)
        print(f"Normalized: {filename}")


