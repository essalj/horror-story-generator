
import os
from moviepy.editor import *

audio_path_0 = r"C:\my\__youtube\videos\sound_effects\asmr_rain.wav"
audio_path = os.path.normpath(audio_path_0)

audio_path_out = 'C:\\my\\__youtube\\videos\\sound_effects'
fn_out = os.path.join(audio_path_out,"rain.mp3")
# Load your WAV file
audio_clip = AudioFileClip(audio_path)

# Write the audio file as MP3
audio_clip.write_audiofile(fn_out)


# creae long rain soundtrack
from moviepy.editor import AudioFileClip, concatenate_audioclips

mp3_in = 'C:\\my\\__youtube\\videos\\sound_effects\\rain_13.mp3'
# List of mp3 files you want to join
mp3_files = [mp3_in, mp3_in, mp3_in, mp3_in, mp3_in]  # Add your file names here

# Load the mp3 files and create audio clips
audio_clips = [AudioFileClip(mp3) for mp3 in mp3_files]

# Concatenate the audio clips
final_clip = concatenate_audioclips(audio_clips)

# Write the result to a new MP3 file
final_clip.write_audiofile("C:\\my\\__youtube\\videos\\sound_effects\\rain_65.mp3")

