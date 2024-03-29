from moviepy.editor import *
from moviepy.editor import AudioFileClip, concatenate_audioclips
from moviepy.audio.fx.all import audio_fadeout

import os
import random

def combine_ambient_tracks(folder_path, video_duration, volume=0.3):
    tracks = []
    audio_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]

    # Shuffle the list of audio files
    random.shuffle(audio_files)

    # Create a single concatenated track from all audio files
    playlist = []
    for file in audio_files:
        audio_clip = AudioFileClip(os.path.join(folder_path, file))
        tracks.append(audio_clip)
        playlist.append(file)

    combined_audio = concatenate_audioclips(tracks)

    # Loop the combined audio to cover the video duration
    looped_audio_duration = 0
    looped_tracks = []
    while looped_audio_duration < video_duration:
        looped_tracks.append(combined_audio)
        looped_audio_duration += combined_audio.duration

    print(playlist)
    # Concatenate the looped audio tracks
    final_combined_audio = concatenate_audioclips(looped_tracks).set_duration(video_duration)
    return final_combined_audio.volumex(volume)


def adjust_volume(audio_clip, target_dBFS=-20.0):
    """
    Adjust the volume of an audio clip to a target dBFS.
    """
    change_in_dBFS = target_dBFS - audio_clip.dBFS
    return audio_clip.volumex(10 ** (change_in_dBFS / 20))

# adjust_volume("C:\\my\\__youtube\\videos\horror_music\\Kirwani - Teental - Aditya Verma, Subir Dev - Copy.mp3", target_dBFS=-20.0)

   

def add_ambient_music_to_video(video_file_path, music_folder_path, output_file_path, music_volume=0.2):
    # Load the original video
    video = VideoFileClip(video_file_path)
    
    # Load and combine ambient music tracks, adjust the volume, and ensure it covers the video duration
    ambient_audio = combine_ambient_tracks(music_folder_path, video.duration, volume=music_volume)

    # Apply fade out to the ambient music over the last 15 seconds
    ambient_audio_with_fadeout = ambient_audio.fx(audio_fadeout, 15)

    # Combine the original audio with the ambient music (now with fade-out)
    final_audio = CompositeAudioClip([video.audio, ambient_audio_with_fadeout])

    # Set the combined audio to the video
    final_video = video.set_audio(final_audio)

    # Write the final video to disk
    final_video.write_videofile(output_file_path, codec='libx264', audio_codec='aac')


# Example usage
# add_ambient_music_to_video(
#     video_file_path=output_final_mp4,
#     music_folder_path='C:\\my\\__youtube\\videos\\horror_music',
#     output_file_path=output_final_mp4_music,
#     music_volume=0.07  # Adjust volume as needed
#     )
    
# The full path

# video_file_path = r"C:\my\__youtube\videos\2024-02-14 Horror compilation - Home Alone vol1_x\home alone stories.mp4"
# path, filename = os.path.split(full_path)
# fn0 = filename.replace(".mp4","")
# fn_out = os.path.join(path,fn0) + " - rain-mp4"

def add_rain_to_video(video_file_path, music_volume =0.1): #, music_folder_path, output_file_path, music_volume=0.3):
# Example usage: add rain asmr
    path, filename = os.path.split(video_file_path)
    fn0 = filename.replace(".mp4","")
    fn_out = os.path.join(path,fn0) + " - rain.mp4"

    add_ambient_music_to_video(
        video_file_path=video_file_path,
        music_folder_path=r"C:\my\__youtube\videos\sound_effects\rain65",
        output_file_path=fn_out,
        music_volume=music_volume  # Adjust volume as needed
        )

# add_rain_to_video(video_file_path = r"C:\my\__youtube\videos\2024-02-26 Ripper compilation\compilation_mp.mp4")
