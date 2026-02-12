import json
import os

def extract_story_and_prompts(file_path):
    """
    Reads a JSON file, extracts the story, image prompts, and gender,
    and returns the directory path and filename without extension.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        tuple: A tuple containing (story_text, image_prompts_list, gender, directory_path, filename_without_extension).
               Returns (None, None, None, None, None) if an error occurs (e.g., file not found,
               invalid JSON, or missing keys).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        story_text = data.get("story")
        image_prompts_list = data.get("image_prompts")
        gender = data.get("gender")

        if story_text is None:
            print(f"Warning: 'story' key not found in {file_path}")
        if image_prompts_list is None:
            print(f"Warning: 'image_prompts' key not found in {file_path}")
            return None, None, None, None, None
        if gender is None:
            print(f"Warning: 'gender' key not found in {file_path}")


        # Split the file path
        directory_path = os.path.dirname(file_path)
        filename_with_extension = os.path.basename(file_path)
        filename_without_extension, _ = os.path.splitext(filename_with_extension)


        return story_text, image_prompts_list, gender, directory_path, filename_without_extension

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None, None, None, None, None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}. Make sure it's a valid JSON file.")
        return None, None, None, None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None, None, None, None


#story, images, gender, path, filename = extract_story_and_prompts('/Users/lasse/Desktop/my/youtube/videos/2025-05-19 cop stories/cop_story_01.json')
