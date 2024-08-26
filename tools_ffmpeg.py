import os
import subprocess

def run_ffmpeg_command(command):
    try:
        subprocess.run(command, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg command failed: {e.stderr.decode()}")
        raise


# convert all files to 1080p
def scale_videos_to_1080p(input_files, width=1920, height=1080):
    output_files = []  # List to store the new filenames

    for fn in input_files:
        # Create the new filename with _1080p added
        fn2 = f"{os.path.splitext(fn)[0]}_1080p{os.path.splitext(fn)[1]}"
        output_files.append(fn2)  # Add the new filename to the list
        
        print(f"Processing: {fn} -> {fn2}")
        
        command = [
            'ffmpeg',
            '-i', fn,
            '-vf', f'scale={width}:{height}',
            '-c:a', 'copy',
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
    '-c', 'copy',
    output_file
    ]
    run_ffmpeg_command(command)
 
    try:
        run_ffmpeg_command(command)
        print(f"Successfully concatenated into: {output_file}")
    except Exception as e:
        print("Error in concat_mp4")



# intro_path = r"C:\my\__youtube\videos\horror_effects\horror video intro 6s.mp4"
# welcome_path = r"C:\my\__youtube\videos\2024-08-18_2342_Scary Stories For Sleep_compilation\clip_0_intro.mp4"
# story_path = r"C:\my\__youtube\videos\2024-08-18_2342_Scary Stories For Sleep_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast.mp4"
# end_path = r"C:\my\__youtube\videos\sound_effects\rain and black screen 10 min.mp4"
# output_path = r"C:\my\__youtube\videos\2024-08-18_2342_Scary Stories For Sleep_compilation\Scary Stories For Sleep With Rain Sounds - True Horror Stories - Fall Asleep Fast_1080.mp4"

    
# input_files =[intro_path, welcome_path, story_path, end_path]
# scaled_files =  scale_videos_to_1080p(input_files)
# concat_mp4(input_files=scaled_files, output_file=output_path)


