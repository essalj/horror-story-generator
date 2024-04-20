from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time
from PIL import Image

def create_silence_audio_clip(silence_duration=2.0):
    silent_array = np.zeros((int(silence_duration * 44100), 2))  # 44100 samples/sec, 2 channels for stereo
    silent_clip = AudioArrayClip(silent_array, fps=44100)
    return silent_clip


def add_silence_to_audio(original_audio_clip, silence_duration=2.0):
    silent_array = np.zeros((int(silence_duration * 44100), 2))  # 44100 samples/sec, 2 channels for stereo
    silent_clip = AudioArrayClip(silent_array, fps=44100)
    return concatenate_audioclips([original_audio_clip, silent_clip])


def create_video_with_images_and_audio(image_paths, audio_path, output_filename='final_video.mp4', fps=30, resolution=(1920, 1080)):
# def create_video_with_images_and_audio(image_paths, audio_path, output_filename='final_video.mp4', fps=30):
    silent_clip = create_silence_audio_clip(silence_duration=2.0)
    audio_clip_in = AudioFileClip(audio_path)
    audio_clip = concatenate_audioclips([silent_clip, audio_clip_in])
    print("audio_clip_in:" + str(audio_clip_in.duration))
    print("silent_clip:" + str(silent_clip.duration))
    print("audio_clip:" + str(audio_clip.duration))
    print(f"Audio durations: Original={audio_clip_in.duration}, Silence={silent_clip.duration}, Total={audio_clip.duration}")
 
    audio_duration = audio_clip.duration

    # Determine the duration for each image and audio segment
    segment_duration = audio_duration / len(image_paths)

    # Create video clips for each image and corresponding audio segments
    video_clips = []
    audio_clips = []

    # for idx, img_path in enumerate(image_paths):
    #     # Create video clip
    #     video_clip = ImageClip(img_path).set_duration(segment_duration)
    #     video_clips.append(video_clip)
    for idx, img_path in enumerate(image_paths):
        video_clip = ImageClip(img_path).set_duration(segment_duration).resize(resolution).set_fps(fps)
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
    # final_video.write_videofile(output_filename, fps=fps)
    final_video.write_videofile(output_filename, fps=fps, codec='libx264')

    # create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)


# # Example usage
# image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg', ...]  # Add your image paths
# audio_path = 'your_audio_file.mp3'
# create_video_with_images_and_audio(image_paths, audio_path)

# image_paths = ['C:\\my\\__youtube\\videos\\2023-12-13_horror\\Ghost in the Machine A Chilling AI Experiment Story - img11.png' , 'C:\\my\\__youtube\\videos\\2023-12-13_horror\\Ghost in the Machine A Chilling AI Experiment Story - img12.png']
# audio_path = "C:\\my\\__youtube\\videos\\2023-12-13_horror\\Ghost in the Machine A Chilling AI Experiment Story - audio_1.mp3"
# create_video_with_images_and_audio(image_paths, audio_path, output_filename='final_video.mp4', fps=30)

# concatenates mp4 files
# def concatenate_videos_old(video_files, output_path):
#     # Load the video clips
#     clips = [VideoFileClip(path) for path in video_files]
#     # clips = [VideoFileClip(os.path.join(xp_path, path)) for path in video_files]
#     final_clip = concatenate_videoclips(clips)
#     final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


# concatenate_videos(mp4_clips, output_final_mp4)
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time

def format_duration(seconds):
    # Convert seconds to a time string of format hh:mm:ss
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def concatenate_videos(video_files, output_path, target_fps=30, target_width=1920, target_height=1080):
# def concatenate_videos(video_files, output_path):
    clips = []
    start_times = []
    current_start = 0

    for index, path in enumerate(video_files):
        try:
            # clip = VideoFileClip(path)
            # Load the video clip with a target resolution and fps
            # clip = VideoFileClip(path).set_fps(target_fps).resize(newsize=(target_width, target_height))
            # clip = VideoFileClip(path).set_fps(target_fps).resize(newsize=(target_width, target_height), resample=Image.Resampling.LANCZOS)
            # clip = VideoFileClip(path).set_fps(target_fps).resize(newsize=(target_width, target_height), resample=Image.Resampling.LANCZOS)
            clip = VideoFileClip(path).set_fps(target_fps).resize((target_width, target_height))

            clips.append(clip)
            start_times.append(f"{index}. {format_duration(current_start)}")
            current_start += clip.duration
        except Exception as e:
            print(f"Error processing {path}: {e}")

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec="libx264")
    
    print("Stories " + " ".join(start_times))
    return start_times

# video_files = mp4_clips
# output_path = output_concat_mp4
# start_times = concatenate_videos(mp4_clips, output_concat_mp4)
# # Example usage:
# video_files = ['video1.mp4', 'video2.mp4', 'video3.mp4']
# output_path = 'output.mp4'
# concatenate_videos(video_files, output_path)

# def concatenate_videos(video_files, output_path):
#     # Initialize a list to hold VideoFileClip objects
#     clips = []
    
#     # for path in video_files:
#     #     try:
#     #         # Load the video clip and ensure it's compatible by setting target resolution and fps
#     #         clip = VideoFileClip(path)
#     #         # Optionally, you can ensure all clips have the same fps and size
#     #         # For example: clip = clip.set_fps(target_fps).resize(new_size=(target_width, target_height))
#     #         clips.append(clip)
#     #     except Exception as e:
#     #         print(f"Error processing {path}: {e}")
    
#     if clips:
#         try:
#             # Concatenate video clips
#             # The method="compose" argument can help avoid size mismatch issues
#             final_clip = concatenate_videoclips(clips, method="compose")
#             # Write the result to a file
#             final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
#         except Exception as e:
#             print(f"Error during concatenation: {e}")
#     else:
#         print("No video clips were successfully loaded.")

# Example usage
# video_files = ['path/to/video1.mp4', 'path/to/video2.mp4']
# output_path = 'path/to/output_video.mp4'
# concatenate_videos(video_files, output_path)
