import os
import subprocess
import tools_add_music_to_mp4 as am
import json

def run_ffmpeg_command(command):
    try:
        result = subprocess.run(command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg command failed: {e.stderr}")
        raise


# convert all files in list to 1080p
def scale_videos_to_1080p(input_files, width=1920, height=1080):
    output_files = []  # List to store the new filenames

    for fn in input_files:
        # Create the new filename with _1080p added
        fn2 = f"{os.path.splitext(fn)[0]}_scaled{os.path.splitext(fn)[1]}"
        output_files.append(fn2)  # Add the new filename to the list
        
        print(f"Processing: {fn} -> {fn2}")
        
        command = [
            'ffmpeg',
            '-i', fn,
            '-vf', f'scale={width}:{height}',
            '-r', '30',
            '-c:a', 'libmp3lame',
            '-q:a', '0',
            fn2
        ]

        try:
            run_ffmpeg_command(command)
            print(f"Successfully scaled: {fn2}")
        except Exception as e:
            print(f"Error processing {fn}: {str(e)}")
            # If there's an error, we'll remove the filename from the output list
            output_files.pop()

    return output_files  # Return the list of successfully processed files
    #k1 = r"C:\my\__youtube\videos\horror_effects\horror video intro 5s.mp4"
    #scale_videos_to_1080p([k1], width=1792, height=1024)
    

def adjust_volume(input_file, output_file, volume=0.28):
    """
    Adjust the volume of a single video file.
    
    :param input_file: Path to the input video file
    :param output_file: Path to save the output video file
    :param volume: Desired volume level (default: 0.28)
    """
    command = [
        'ffmpeg',
        '-i', input_file,
        '-filter:a', f"volume={volume}",
        '-c:v', 'copy',
        output_file
    ]

    try:
        subprocess.run(command, check=True, stderr=subprocess.PIPE)
        print(f"Successfully adjusted volume: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error adjusting volume: {e.stderr.decode()}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

# Example usage:
# adjust_volume('input.mp4', 'output.mp4')
# Or to set a different volume:
# adjust_volume('input.mp4', 'output.mp4', volume=0.5)


# create concatenated mp4
def concat_mp4(input_files, output_file): # multiple files
    # Create a temporary file with the names of input files
    with open('concat_list.txt', 'w') as f:
        for i in input_files:
            f.write(f"file '{i}'\n")

    # command to concat files with ffmpeg
    command = [
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', 'concat_list.txt',
    '-c', 'copy', '-y',
    output_file
    ]
    try:
        run_ffmpeg_command(command)
        print(f"Successfully concatenated into: {output_file}")
        return True, input_files
    except Exception as e:
        print(f"Error in concat_mp4: {e}")
        return False, input_files


def cut_video(input_file, output_file, start_time, duration):
    """
    Cut a video to a specified length.
    
    :param input_file: Path to the input video file
    :param output_file: Path to save the output video file
    :param start_time: Start time of the cut in format HH:MM:SS
    :param duration: Duration of the cut in format HH:MM:SS
    """
    command = [
        'ffmpeg',
        '-ss', start_time,
        '-i', input_file,
        '-t', duration,
        '-c', 'copy',
        output_file
    ]

    try:
        run_ffmpeg_command(command)
        print(f"Successfully cut video: {output_file}")
    except Exception as e:
        print(f"Error cutting video {input_file}: {str(e)}")
# cut_video('/Users/lasse/Desktop/my/youtube/2024-09-21_1531_Truly Scary Ouija Stories_compilation/Truly Scary Ouija Stories - rain_sleep.mp4',
#           '/Users/lasse/Desktop/my/youtube/2024-09-21_1531_Truly Scary Ouija Stories_compilation/Truly Scary Ouija Stories - rain_sleep_cut.mp4', 
#           "00:00:00", "06:59:59")


def add_background_sound(input_video, background_sound, output_video, bg_volume=0.1):
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video file not found: {input_video}")
    if not os.path.exists(background_sound):
        raise FileNotFoundError(f"Background sound file not found: {background_sound}")
    
    command = [
        'ffmpeg',
        '-i', input_video,
        '-i', background_sound,
        '-filter_complex',
        f'[1:a]volume={bg_volume}[bg];[0:a][bg]amix=inputs=2:duration=longest',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        output_video
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully added background sound to: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr}")
    except Exception as e:
        print(f"Error in add_background_sound: {str(e)}")


def add_background_sound_with_loop(input_video, background_sound, output_video, bg_volume=0.07):
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video file not found: {input_video}")
    if not os.path.exists(background_sound):
        raise FileNotFoundError(f"Background sound file not found: {background_sound}")

    video_duration = get_duration_mp4(input_video)
    audio_duration = get_duration_mp4(background_sound)

    if video_duration > audio_duration:
        loop_count = int(video_duration / audio_duration) + 1
        # Create a temporary file for the looped audio
        temp_audio_file = "temp_looped_audio.mp3"
        
        # Create a file list for ffmpeg
        with open("concat_list.txt", "w") as f:
            for _ in range(loop_count):
                f.write(f"file '{background_sound}'\n")
        
        # Concatenate audio files to create a looped version
        concat_command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', 'concat_list.txt',
            '-c', 'copy', '-y',
            temp_audio_file
        ]
        run_ffmpeg_command(concat_command)
        
        background_sound = temp_audio_file

    command = [
        'ffmpeg',
        '-i', input_video,
        '-i', background_sound,
        '-filter_complex',
        f'[1:a]volume={bg_volume}[bg];[0:a][bg]amix=inputs=2:duration=longest',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        output_video
    ]

    try:
        subprocess.run(command, check=True, text=True)
        print(f"Successfully added background sound to: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr}")
    except Exception as e:
        print(f"Error in add_background_sound_with_loop: {str(e)}")
    finally:
        # Clean up temporary files
        if 'temp_audio_file' in locals() and os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
        if os.path.exists("concat_list.txt"):
            os.remove("concat_list.txt")

def concatenate_videos_ffmpeg_demuxer(input_files, output_file):
    """
    Concatenates multiple video files using the FFmpeg concat demuxer.

    Args:
        input_files (list): A list of paths to the input video files.
        output_file (str): The path for the output concatenated video file.
    """
    list_file_path = 'concat_list.txt'
    with open(list_file_path, 'w') as f:
        for fpath in input_files:
            f.write(f"file '{fpath}'\n")

    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental', # Needed for some AAC encoding
        output_file
    ]

    try:
        run_ffmpeg_command(command)
        print(f"Successfully concatenated videos into: {output_file}")
    except Exception as e:
        print(f"Error concatenating videos: {str(e)}")
    finally:
        # Clean up the temporary list file
        if os.path.exists(list_file_path):
            os.remove(list_file_path)


def get_duration_mp4(file_path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = json.loads(result.stdout)
    return float(data['format']['duration'])


# output_concat_mp4 = r"C:\my\__youtube\videos\2024-10-13_1857_Truly Scary Halloween Stories_compilation\Truly Scary Halloween Stories.mp4"
      
# print("Adding rain sound...")
# am.add_rain_to_video(video_file_path=output_concat_mp4, music_volume=0.28)


# Example usage
if __name__ == "__main__":
    input_video = r"C:\my\__youtube\videos\2024-10-13_1857_Truly Scary Halloween Stories_compilation\Truly Scary Halloween Stories.mp4"
    background_sound = r"C:\my\__youtube\videos\sound_effects\rain65\rain_65.mp3"
    output_video = r"C:\my\__youtube\videos\2024-10-13_1857_Truly Scary Halloween Stories_compilation\Truly Scary Halloween Stories_rain.mp4"

    add_background_sound(input_video, background_sound, output_video)

# # intro_path = r"C:\my\__youtube\videos\horror_effects\horror video intro 6s.mp4"
# welcome_path = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\clip_0_intro - rain.mp4"
# story_path = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Truly Scary Ouija Stories - rain.mp4"
# end_path = r"C:\my\__youtube\videos\sound_effects\rain and black screen 10 min_1080p.mp4"
# output_path = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast_1080.mp4"


#######################################
# project coombine files to full video
# scale_videos_to_1080p([welcome_path], width=1920, height=1080)
# scale_videos_to_1080p([story_path], width=1920, height=1080)

# create 370min rain vol 028
# rain10 = r"C:\my\__youtube\videos\sound_effects\rain and black screen 10 min_1080p.mp4"
# rain10v = r"C:\my\__youtube\videos\sound_effects\rain and black screen 10 min_1080p_v028.mp4"
# adjust_volume(rain10, rain10v)
# input_files = [rain10v] * 37
# output_file = r"C:\my\__youtube\videos\sound_effects\rain and black screen 370 min_1080p.mp4"
# concat_mp4(input_files, output_file)


#create full movie
# welcome_path = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\clip_0_intro - rain_1080p.mp4"
# story_path = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Truly Scary Ouija Stories - rain_1080p.mp4"
# end_path =  r"C:\my\__youtube\videos\sound_effects\rain and black screen 370 min_1080p.mp4"
# output_file = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast_1080 vol028.mp4"
# concat_mp4(input_files, output_file)

# input_f = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast_1080 vol028.mp4"
# output_f = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast_1080 vol028 cutx.mp4"
# cut_video(input_f, output_f, start_time="00:00:00", duration="07:07:06.51")

# cut_video(input_file=r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast_1080.mp4",
#           output_file = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast_1080 vol28.mp4", 
#           start_time="00:00:00", duration="07:07:06.51")

# input_files =[intro_mp4]
# input_files =[welcome_path, story_path, end_path]
# scaled_files =  scale_videos_to_1080p(input_files)
# concat_mp4(input_files=scaled_files, output_file=output_path)


# cut_video(input_file, output_file, start_time, duration)

# cut_video(input_file=r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast_1080.mp4",
#           output_file = r"C:\my\__youtube\videos\2024-09-03_1820_Truly Scary Ouija Stories_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast_1080 vol28.mp4", 
#           start_time="00:00:00", duration="07:07:06.51")
