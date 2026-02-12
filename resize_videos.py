import os
import tools_ffmpeg as tff

def resize_videos_in_directory(input_dir, output_dir, size=(1920, 1080)):
    """
    Resizes all MP4 videos in a directory to a specified size using tools_ffmpeg.py.

    Args:
        input_dir (str): Path to the directory containing input video files.
        output_dir (str): Path to save the resized video files.
        size (tuple): The desired output size as (width, height). Defaults to 1920x1080.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    input_files = []
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path) and filename.lower().endswith(('.mp4')):
            input_files.append(input_path)
        else:
            print(f"Skipping non-MP4 file: {filename}")

    if not input_files:
        print(f"No MP4 files found in {input_dir}")
        return

    print(f"Resizing videos in '{input_dir}' to {size} and saving to '{output_dir}'")
    
    # Use the scale_videos_to_1080p function from tools_ffmpeg.py
    # It handles creating new filenames with _1080p, so we'll adjust the output path
    # size = [1792, 1024]
    scaled_files = tff.scale_videos_to_1080p(input_files, width=size[0], height=size[1])
    #scaled_files = tff.scale_videos_to_1080p(i1, width=size[0], height=size[1])

    # Move the scaled files to the specified output directory
    for original_path, scaled_path in zip(input_files, scaled_files):
        filename = os.path.basename(scaled_path)
        final_output_path = os.path.join(output_dir, filename)
        try:
            os.rename(scaled_path, final_output_path)
            print(f"Moved scaled file to: {final_output_path}")
        except Exception as e:
            print(f"Error moving scaled file {scaled_path} to {final_output_path}: {e}")

resize_videos_in_directory(input_dir, output_dir, size=(1920, 1080))

if __name__ == "__main__":
    # Example Usage:
    # Create a dummy input directory and add some dummy files if needed
    # import shutil
    # try:
    #     os.makedirs("input_videos", exist_ok=True)
    #     os.makedirs("output_videos", exist_ok=True)
    #     # You would need actual small MP4 files here for testing
    #     # Example: shutil.copy('path/to/your/dummy.mp4', 'input_videos/dummy1.mp4')
    #     print("Created dummy video directories. Please add MP4 files to 'input_videos'.")
    # except Exception as e:
    #     print(f"Error creating dummy directories: {e}")

    # --- Uncomment the section below to run the resizing ---

    # input_directory = "input_videos" # Replace with your input directory
    # output_directory = "output_videos" # Replace with your output directory
    # target_size = (1920, 1080) # Desired size (width, height)

    # print(f"Resizing videos in '{input_directory}' to {target_size} and saving to '{output_directory}'")
    # resize_videos_in_directory(input_directory, output_directory, target_size)
    # print("Video resizing process finished.")

    print("Script created. Please uncomment the example usage section and modify the input/output directories and target size as needed.")


