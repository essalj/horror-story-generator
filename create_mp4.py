from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np

def add_silence_to_audio(original_audio_clip, silence_duration=2.0):
    silent_array = np.zeros((int(silence_duration * 44100), 2))  # 44100 samples/sec, 2 channels for stereo
    silent_clip = AudioArrayClip(silent_array, fps=44100)
    return concatenate_audioclips([original_audio_clip, silent_clip])

def create_video_with_images_and_audio(image_paths, audio_path, output_filename='final_video.mp4', fps=30):
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration

    # Determine the duration for each image and audio segment
    segment_duration = audio_duration / len(image_paths)

    # Create video clips for each image and corresponding audio segments
    video_clips = []
    audio_clips = []
    for idx, img_path in enumerate(image_paths):
        # Create video clip
        video_clip = ImageClip(img_path).set_duration(segment_duration)
        video_clips.append(video_clip)

        # Create corresponding audio segment
        start_time = idx * segment_duration
        end_time = start_time + segment_duration
        audio_segment = audio_clip.subclip(start_time, end_time)
        audio_clips.append(audio_segment)

    # Concatenate all video and audio clips
    concatenated_video = concatenate_videoclips(video_clips, method="compose")
    concatenated_audio = concatenate_audioclips(audio_clips)

    # Add 2 seconds of silence at the end of the audio
    final_audio = add_silence_to_audio(concatenated_audio, 2.0)

    # Set the concatenated audio to the video
    final_video = concatenated_video.set_audio(final_audio)
    final_video.write_videofile(output_filename, fps=fps)

# # Example usage
# image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg', ...]  # Add your image paths
# audio_path = 'your_audio_file.mp3'
# create_video_with_images_and_audio(image_paths, audio_path)

# image_paths = ['C:\\my\\__youtube\\videos\\2023-12-13_horror\\Ghost in the Machine A Chilling AI Experiment Story - img11.png' , 'C:\\my\\__youtube\\videos\\2023-12-13_horror\\Ghost in the Machine A Chilling AI Experiment Story - img12.png']
# audio_path = "C:\\my\\__youtube\\videos\\2023-12-13_horror\\Ghost in the Machine A Chilling AI Experiment Story - audio_1.mp3"
# create_video_with_images_and_audio(image_paths, audio_path, output_filename='final_video.mp4', fps=30)

# concatenates mp4 files
def concatenate_videos(video_files, output_path):
    # Load the video clips
    clips = [VideoFileClip(path) for path in video_files]
    # clips = [VideoFileClip(os.path.join(xp_path, path)) for path in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

