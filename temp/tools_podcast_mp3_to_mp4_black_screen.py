from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip


def mp3_to_mp4(mp3_file, output_file, duration=None):
    # Load the audio file
    audio = AudioFileClip(mp3_file)
    
    # If duration is not specified, use the audio duration
    if duration is None:
        duration = audio.duration

    # Create a dark background clip
    width, height = 1280, 720 # You can adjust these values
    color = (0, 0, 0)  # RGB for black
    bg_clip = ColorClip(size=(width, height), color=color, duration=duration)

    # Combine the audio with the background
    video = CompositeVideoClip([bg_clip])
    video = video.set_audio(audio)

    # Write the result to a file
    video.write_videofile(output_file, fps=24)

# Usage
mp3_file = r"C:\my\__youtube\videos\2024-07-20_2243_Truly Scary Ouija Stories_compilation\Truly Scary Ouija Stories - rain.mp3"
output_file = r"C:\my\__youtube\videos\2024-07-20_2243_Truly Scary Ouija Stories_compilation\Truly Scary Ouija Stories - rain_black screen.mp4"

mp3_to_mp4(mp3_file, output_file)


# # Usage
# input_mp4 = r"C:\my\__youtube\videos\2024-07-20_2243_Truly Scary Ouija Stories_compilation\Truly Scary Ouija Stories - rain.mp4"
# output_mp3 = r"C:\my\__youtube\videos\2024-07-20_2243_Truly Scary Ouija Stories_compilation\Truly Scary Ouija Stories - rain.mp3"
# ```

