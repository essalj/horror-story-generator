import os
import subprocess
import tools_create_mp4 as tcm

# Replace these with the actual paths to your video and audio files
VIDEO_FILES = [
    r"C:\my\__youtube\videos\2024-07-04_1609_Truly Scary Ouija Stories_compilation\clip_0_intro.mp4",
    r"C:\my\__youtube\videos\2024-07-04_1609_Truly Scary Ouija Stories_compilation\clip_0_intro.mp4",
    r"C:\my\__youtube\videos\2024-07-04_1609_Truly Scary Ouija Stories_compilation\clip_0_intro.mp4"
    ]

end_sound_file = r"C:\my\__youtube\videos\_horror_effects\Cartoon Cowbell.mp3"  # Replace with your actual sound effect file path

INCITE_AUDIO_FILE = r"C:\my\__youtube\videos\_horror_effects\002_incite_audio.mp3"
INCITE_VIDEO_FILE = r"C:\my\__youtube\videos\_horror_effects\incite_coffee.mp4"
OUTPUT_DIR = r"C:\my\__youtube\videos\Horror_stories_test"

def concatenate_and_play():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output_path = os.path.join(OUTPUT_DIR, "concatenated_output_with_incite.mp4")
    
    print("Concatenating videos with incite clip...")
    start_times = tcm.concatenate_videos(
        VIDEO_FILES, 
        output_path, 
        end_sound_file,
        incite_audio_path=INCITE_AUDIO_FILE,
        incite_video_path=INCITE_VIDEO_FILE,
        incite_position=1  # This will insert after the first story
    )
    
    print("\nConcatenation complete.")
    print(f"Output file: {output_path}")
    print("\nStart times of each clip:")
    for i, time in enumerate(start_times):
        print(f"Video {i+1}: {time}")
    
    # Attempt to play the video
    print("\nAttempting to play the concatenated video...")
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(output_path)
        elif os.name == 'posix':  # For macOS and Linux
            opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
            subprocess.call([opener, output_path])
    except Exception as e:
        print(f"Couldn't automatically play the video: {e}")
        print(f"Please manually open the file: {output_path}")

# if __name__ == "__main__":
#     concatenate_and_play()