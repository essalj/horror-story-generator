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


# usecase: add chime in end of story... add incite to coffe and subscribe in end of story 1
def add_end_sound(video_clip, sound_effect_path, duration=2.0):
    # Load the sound effect
    sound_effect = AudioFileClip(sound_effect_path).subclip(0, duration)
    
    # Get the original audio
    original_audio = video_clip.audio
    
    # Calculate the start time for the sound effect
    start_time = video_clip.duration - duration
    
    # Combine the original audio with the sound effect
    new_audio = CompositeAudioClip([
        original_audio,
        sound_effect.set_start(start_time)
    ])
    
    # Set the new audio to the video clip
    return video_clip.set_audio(new_audio)


def create_video_with_images_and_audio(image_paths, audio_path, output_filename='final_video.mp4', fps=30):
    silent_clip = create_silence_audio_clip(silence_duration=2.0)
    audio_clip_in = AudioFileClip(audio_path)
    audio_clip = concatenate_audioclips([silent_clip, audio_clip_in])
    print("audio_clip_in:" + str(audio_clip_in.duration))
    print("silent_clip:" + str(silent_clip.duration))
    print("audio_clip:" + str(audio_clip.duration))

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
    concatenated_video = concatenate_videoclips(video_clips)
    # concatenated_video = concatenate_videoclips(video_clips, method="compose")
    concatenated_audio = concatenate_audioclips(audio_clips)

    # Add 2 seconds of silence at the end of the audio
    final_audio = add_silence_to_audio(concatenated_audio, 2.0)

    # Set the concatenated audio to the video
    final_video = concatenated_video.set_audio(final_audio)
    final_video.write_videofile(output_filename, fps=fps)

    # create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)
    # # Example usage
    # image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg', ...]  # Add your image paths
    # audio_path = 'your_audio_file.mp3'
    # create_video_with_images_and_audio(image_paths, audio_path)

    # image_paths = ['C:\\my\\__youtube\\videos\\2023-12-13_horror\\Ghost in the Machine A Chilling AI Experiment Story - img11.png' , 'C:\\my\\__youtube\\videos\\2023-12-13_horror\\Ghost in the Machine A Chilling AI Experiment Story - img12.png']
    # audio_path = "C:\\my\\__youtube\\videos\\2023-12-13_horror\\Ghost in the Machine A Chilling AI Experiment Story - audio_1.mp3"
    # create_video_with_images_and_audio(image_paths, audio_path, output_filename='final_video.mp4', fps=30)



# concatenate_videos(mp4_clips, output_final_mp4)
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time

def format_duration(seconds):
    # Convert seconds to a time string of format hh:mm:ss
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ColorClip

def concatenate_videos(video_files, output_path, end_sound_path=None, incite_audio_path=None, incite_video_path=None, incite_position=2):
    clips = []
    start_times = []
    current_start = 0

    for index, path in enumerate(video_files):
        try:
            clip = VideoFileClip(path)
            
            # Add a 2-second pause at the end of each clip
            pause_clip = ColorClip(size=clip.size, color=(0, 0, 0), duration=2)
            pause_clip = pause_clip.set_audio(None)  # Ensure the pause is silent
            
            combined_clip = concatenate_videoclips([clip, pause_clip])
            clips.append(combined_clip)
            
            start_times.append(f"{index}. {format_duration(current_start)}")
            current_start += combined_clip.duration

            # Insert incite clip after the specified position
            if index + 1 == incite_position and incite_audio_path and incite_video_path:
                incite_video = VideoFileClip(incite_video_path)
                incite_audio = AudioFileClip(incite_audio_path)
                
                # If video is shorter than audio, extend it
                if incite_video.duration < incite_audio.duration:
                    incite_video = incite_video.fx(vfx.loop, duration=incite_audio.duration)
                # If video is longer, trim it
                else:
                    incite_video = incite_video.subclip(0, incite_audio.duration)
                
                incite_clip = incite_video.set_audio(incite_audio)
                clips.append(incite_clip)
                current_start += incite_clip.duration

            # Add end sound clip after each video except the last one
            if end_sound_path and index < len(video_files) - 1:
                sound_clip = AudioFileClip(end_sound_path)
                silent_clip = ColorClip(size=clip.size, color=(0, 0, 0), duration=sound_clip.duration)
                silent_clip = silent_clip.set_audio(sound_clip)
                clips.append(silent_clip)
                current_start += sound_clip.duration

        except Exception as e:
            print(f"Error processing {path}: {e}")
    
    if clips:
        try:
            final_clip = concatenate_videoclips(clips, method="compose")
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        except Exception as e:
            print(f"Error during concatenation: {e}")
    else:
        print("No video clips were successfully loaded.")
    
    print("Stories " + " ".join(start_times))
    return start_times

