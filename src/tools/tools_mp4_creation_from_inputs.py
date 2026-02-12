import os
import datetime
import tools_file_operations as tfo
from flow_1a_create_mp4_story import create_images, create_voice_over, create_mp4

def create_mp4_from_inputs(story, image_prompts, gender, title="generated_story"):
    """
    Creates an MP4 story directly from provided story text, image prompts, and gender.
    This function bypasses the story generation and prompt generation steps.

    Args:
        story (str): The full story text.
        image_prompts (list): A list of image prompts for each action beat.
        gender (str): The gender for the voice-over ("male" or "female").
        title (str): Optional title for the output file.

    Returns:
        str: The path to the generated MP4 file, or None if an error occurred.
    """
    break_line = "\n"
    xp_path_0 = '/Users/lasse/Desktop/my/youtube' #mac
    xp_path = tfo.create_dated_folder(xp_path_0, "custom_story")
    os.makedirs(xp_path, exist_ok=True)

    fn = title # Use the provided title as the base filename

    if story is None or not image_prompts or gender is None:
        print("Missing story, image prompts, or gender. Exiting.")
        return None

    count_action_beats = len(image_prompts)
    image_files = []
    error_list = []

    # Call create_images with the provided prompts
    create_images(image_prompts, count_action_beats, xp_path, fn, error_list, image_files)

    # Call create_voice_over with the provided story and gender
    audio_file = create_voice_over(story, gender, xp_path, fn)

    # Call create_mp4 with the generated files
    output_final_mp4 = create_mp4(image_files, audio_file, xp_path, fn)

    print(f"\nMP4 creation process finished for custom story.")
    print(f"Output MP4: {output_final_mp4}")
    if error_list:
        print("\nErrors encountered:")
        for error in error_list:
            print(f"- {error}")
    return output_final_mp4
