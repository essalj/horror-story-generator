from moviepy import *
#from moviepy.editor import AudioFileClip, concatenate_audioclips
#from moviepy.audio.fx.all import audio_fadeout

import os
import random


def combine_ambient_tracks(folder_path, video_duration, volume=0.3):
    tracks = []
    audio_files = [file for file in os.listdir(folder_path) if file.endswith(".mp3")]

    if not audio_files:
        raise ValueError(f"No MP3 files found in {folder_path}")

    # Shuffle the list of audio files
    random.shuffle(audio_files)

    # Create a single concatenated track from all audio files
    playlist = []
    for file in audio_files:
        try:
            full_path = os.path.join(folder_path, file)
            print(f"Loading audio file: {full_path}")
            audio_clip = AudioFileClip(full_path)
            
            # Verify the audio clip loaded properly
            if audio_clip is None or not hasattr(audio_clip, 'duration'):
                print(f"Warning: Could not properly load {file}")
                continue
                
            print(f"Successfully loaded {file} (duration: {audio_clip.duration}s)")
            tracks.append(audio_clip)
            playlist.append(file)
        except Exception as e:
            print(f"Error loading {file}: {str(e)}")
            continue

    if not tracks:
        raise ValueError("No valid audio tracks could be loaded")

    print(f"Successfully loaded {len(tracks)} audio tracks")
    
    # Create a single audio clip from the first track
    if len(tracks) == 1:
        base_audio = tracks[0]
    else:
        base_audio = concatenate_audioclips(tracks)
    
    print(f"Base audio duration: {base_audio.duration}s")
    print(f"Required duration: {video_duration}s")
    
    # Loop the audio to cover the video duration
    num_loops = int(video_duration / base_audio.duration) + 1
    looped_tracks = []
    for _ in range(num_loops):
        looped_tracks.append(base_audio)
    
    print(f"Creating {num_loops} loops of the base audio")
    final_audio = concatenate_audioclips(looped_tracks)
    
    # Trim to exact duration
    final_audio = final_audio.subclip(0, video_duration)
    print(f"Final audio duration: {final_audio.duration}s")
    
    print(playlist)
    return final_audio.volumex(volume)


def adjust_volume(audio_clip, target_dBFS=-20.0):
    """
    Adjust the volume of an audio clip to a target dBFS.
    """
    change_in_dBFS = target_dBFS - audio_clip.dBFS
    return audio_clip.volumex(10 ** (change_in_dBFS / 20))

def add_ambient_music_to_video(video_file_path, music_folder_path, output_file_path, music_volume=0.2):
    # Verify input paths exist
    if not os.path.exists(video_file_path):
        raise FileNotFoundError(f"Video file not found: {video_file_path}")
    if not os.path.exists(music_folder_path):
        raise FileNotFoundError(f"Music folder not found: {music_folder_path}")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    print(f"Loading video: {video_file_path}")
    # Load the original video
    video = VideoFileClip(video_file_path)
    
    print("Combining ambient tracks...")
    # Load and combine ambient music tracks, adjust the volume, and ensure it covers the video duration
    ambient_audio = combine_ambient_tracks(music_folder_path, video.duration, volume=music_volume)

    # Apply fade out to the ambient music over the last 15 seconds
    ambient_audio_with_fadeout = ambient_audio.fx(audio_fadeout, 15)

    # Create the final audio
    if video.audio is not None:
        final_audio = CompositeAudioClip([video.audio, ambient_audio_with_fadeout])
    else:
        final_audio = ambient_audio_with_fadeout

    # Set the combined audio to the video
    final_video = video.set_audio(final_audio)

    print(f"Writing output to: {output_file_path}")
    # Write the final video to disk
    final_video.write_videofile(output_file_path, codec='libx264', audio_codec='aac')
    
    # Clean up
    video.close()
    if video.audio is not None:
        video.audio.close()
    ambient_audio.close()
    final_video.close()


def add_rain_to_video(video_file_path, music_volume=0.1):
    """Add rain sound effects to a video."""
    path, filename = os.path.split(video_file_path)
    fn0 = filename.replace(".mp4","")
    fn_out = os.path.join(path, fn0) + " - rain.mp4"

    # Use absolute path to rain effects (works on both Mac and Windows)
    rain_folder = os.path.expanduser("~/Desktop/my/youtube/videos/sound_effects/rain_folder")
    if not os.path.exists(rain_folder):
        # Fallback to effects/audio folder
        rain_folder = os.path.join(os.path.dirname(__file__), "..", "..", "effects", "audio")
    
    add_ambient_music_to_video(
        video_file_path=video_file_path,
        music_folder_path=rain_folder,
        output_file_path=fn_out,
        music_volume=music_volume
    )
    return fn_out


def add_suno_music_to_video(video_file_path, music_folder_path=None, output_file_path=None, music_volume=0.2):
    """Add Suno AI-generated music to a video.
    
    Args:
        video_file_path: Path to input video
        music_folder_path: Path to folder with MP3 files (defaults to effects/audio/)
        output_file_path: Path for output video (optional)
        music_volume: Volume level (0.0 to 1.0)
    """
    if music_folder_path is None:
        # Default to effects/audio folder which includes both suno_2024 and suno_2025
        music_folder_path = os.path.join(os.path.dirname(__file__), "..", "..", "effects", "audio")
    
    if output_file_path is None:
        path, filename = os.path.split(video_file_path)
        fn0 = filename.replace(".mp4","")
        output_file_path = os.path.join(path, fn0) + " - with_suno_music.mp4"
    
    add_ambient_music_to_video(
        video_file_path=video_file_path,
        music_folder_path=music_folder_path,
        output_file_path=output_file_path,
        music_volume=music_volume
    )
    return output_file_path

# ex.
# add_ambient_music_to_video(
#       video_file_path=r"C:\my\__youtube\videos\sound_effects\black screen_60min_1080p.mp4",
#       music_folder_path=r"C:\my\__youtube\videos\sound_effects\meditation_music",
#       output_file_path=r"C:\my\__youtube\videos\sound_effects\meditation_music_black screen_60min_1080p.mp4",
#       music_volume=0.15  # Adjust volume as needed
#       )
