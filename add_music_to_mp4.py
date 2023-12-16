from moviepy.editor import *
import os
import random

def combine_ambient_tracks(folder_path, video_duration, volume=0.3):
    tracks = []
    audio_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]

    # Shuffle the list of audio files
    random.shuffle(audio_files)

    # Create a single concatenated track from all audio files
    for file in audio_files:
        audio_clip = AudioFileClip(os.path.join(folder_path, file))
        tracks.append(audio_clip)

    combined_audio = concatenate_audioclips(tracks)

    # Loop the combined audio to cover the video duration
    looped_audio_duration = 0
    looped_tracks = []
    while looped_audio_duration < video_duration:
        looped_tracks.append(combined_audio)
        looped_audio_duration += combined_audio.duration

    # Concatenate the looped audio tracks
    final_combined_audio = concatenate_audioclips(looped_tracks).set_duration(video_duration)

    return final_combined_audio.volumex(volume)



def add_ambient_music_to_video(video_file_path, music_folder_path, output_file_path, music_volume=0.3):
    # Load the original video
    video = VideoFileClip(video_file_path)
    
    # Load and combine ambient music tracks, adjust the volume, and ensure it covers the video duration
    ambient_audio = combine_ambient_tracks(music_folder_path, video.duration, volume=music_volume)

    # Combine the original audio with the ambient music
    final_audio = CompositeAudioClip([video.audio, ambient_audio])

    # Set the combined audio to the video
    final_video = video.set_audio(final_audio)

    # Write the final video to disk
    final_video.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

# Example usage
# 





















































