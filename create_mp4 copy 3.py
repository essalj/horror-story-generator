# pip install moviepy

from moviepy.editor import *
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import AudioFileClip, concatenate_audioclips
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np



def add_silence_to_audio(original_audio_clip, silence_duration=2.0):
    silent_array = np.zeros((int(silence_duration * 44100), 2))  # 44100 samples/sec, 2 channels for stereo
    silent_clip = AudioArrayClip(silent_array, fps=44100)
    final_audio = concatenate_audioclips([original_audio_clip, silent_clip])
    return final_audio
    
# silence_duration= 2
def create_video_with_audio(xp_path, image_paths, audio_path, output_filename='final_video.mp4', fps=30, silence_duration = 2):
    # add silence between clips
audio_clip = AudioFileClip(audio_path)
audio_clip = add_silence_to_audio(audio_clip, silence_duration=silence_duration) # add 2 sec silence between chapters
audio_duration = audio_clip.duration
clip_duration = audio_duration / len(image_path) # time pr image

# Set the background image with the duration of the audio pr. image
# Create individual video clips for each image
temp_video_files = []
for idx, image_path_ in enumerate(image_paths):
    print(idx, image_path)
    # temp_output_path = f"temp_clip_{idx}.mp4"
    # create_individual_video_clip(image_path, clip_duration, temp_output_path, fps)
    temp_video_files.append(temp_output_path)
    bg_image = ImageClip(image_path).set_duration(audio_duration)
    final_video = bg_image.set_audio(audio_clip)     # Add the audio to the video


# Write the final video to a file
final_video.write_videofile(output_filename, fps=fps)
# create_video_with_audio(image_path = image_path, audio_path = audio_path, output_filename=output_mp4, fps=30, silence_duration=2)


def concatenate_videos(video_files, output_path):
    # Load the video clips
    clips = [VideoFileClip(path) for path in video_files]
    # clips = [VideoFileClip(os.path.join(xp_path, path)) for path in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage:
# video_files = [output_filename, output_filename,output_filename]
#concatenate_videos(video_files, 'C:\\my\\__youtube\\videos\\2023-12-10_horror\\concat_video.mp4')
# xp_path = 'C:\\my\\__youtube\\videos\\2023-12-10_horror'  #\\clip_0.mp4'
# output_filename = 'clip_0.mp4'
