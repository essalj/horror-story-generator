from moviepy.editor import *
import numpy as np
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import AudioFileClip, concatenate_audioclips
from moviepy.audio.AudioClip import AudioArrayClip



def add_silence_to_audio(original_audio_clip, silence_duration=2.0):
    silent_array = np.zeros((int(silence_duration * 44100), 2))  # 44100 samples/sec, 2 channels for stereo
    silent_clip = AudioArrayClip(silent_array, fps=44100)
    final_audio = concatenate_audioclips([original_audio_clip, silent_clip])
    return final_audio

def create_individual_video_clip(image_path, clip_duration, output_path, fps=30):
    # Create a video clip from a single image
    clip = ImageClip(image_path).set_duration(clip_duration)
    clip.write_videofile(output_path, fps=fps)

def concatenate_videos(video_files, output_path):
    # Load the video clips
    clips = [VideoFileClip(path) for path in video_files]
    # clips = [VideoFileClip(os.path.join(xp_path, path)) for path in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


def create_video_with_images_and_audio(image_paths, audio_path, output_filename='final_video.mp4', fps=30):
    # Calculate duration of each image clip based on the audio duration
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    clip_duration = audio_duration / len(image_paths)

    # Create individual video clips for each image
    temp_video_files = []
    for idx, image_path in enumerate(image_paths):
        temp_output_path = f"temp_clip_{idx}.mp4"
        create_individual_video_clip(image_path, clip_duration, temp_output_path, fps)
        temp_video_files.append(temp_output_path)

    # Concatenate all video clips
    concatenate_videos(temp_video_files, output_filename)

    # Add the audio to the final video
    final_clip = VideoFileClip(output_filename)
    final_clip = final_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_filename, fps=fps)

    # Cleanup temporary files
    for file in temp_video_files:
        os.remove(file)

# # Example usage
# image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg', ...]  # Add your image paths
# audio_path = 'your_audio_file.mp3'
# create_video_with_images_and_audio(image_paths, audio_path)
