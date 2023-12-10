# pip install moviepy

from moviepy.editor import *
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import AudioFileClip, concatenate_audioclips
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np




# audio_path = "C:\\my\\__youtube\\videos\\2023-12-10_horror\\Lured into Darkness The Psychological Web of the AI Girlfriend - thanks - audio_99.mp3"
# image_path = "C:\\my\\__youtube\\videos\\2023-12-10_horror\\Lured into Darkness The Psychological Web of the AI Girlfriend - ytmb1.png"
# output_filename = "C:\\my\\__youtube\\videos\\2023-12-10_horror\\final_video.mp4"
# fps = 30


def add_silence_to_audio(original_audio_clip, silence_duration=2.0):
    silent_array = np.zeros((int(silence_duration * 44100), 2))  # 44100 samples/sec, 2 channels for stereo
    silent_clip = AudioArrayClip(silent_array, fps=44100)
    final_audio = concatenate_audioclips([original_audio_clip, silent_clip])
    return final_audio
    

def create_video_with_audio(image_path, audio_path, output_filename='final_video.mp4', fps=30, silence_duration = 2):
    # add silence between clips
    audio_clip = AudioFileClip(audio_path)
    audio_clip = add_silence_to_audio(audio_clip, silence_duration=silence_duration)
    audio_duration = audio_clip.duration

    # Set the background image with the duration of the audio
    bg_image = ImageClip(image_path).set_duration(audio_duration)

    # Add the audio to the video
    final_video = bg_image.set_audio(audio_clip)

    # Write the final video to a file
    final_video.write_videofile(output_filename, fps=fps)
#create_video_with_audio(image_path = image_path, audio_path = audio_path, output_filename=output_filename, fps=30, silence_duration = 2)


def concatenate_videos(video_path1, video_path2, output_path):
    # Load the video clips
    clip1 = VideoFileClip(video_path1)
    clip2 = VideoFileClip(video_path2)
    final_clip = concatenate_videoclips([clip1, clip2])

    # Write the result to a file
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage:
#concatenate_videos(output_filename, output_filename, 'C:\\my\\__youtube\\videos\\2023-12-10_horror\\concat_video.mp4')
