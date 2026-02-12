import datetime
import os
import re
import json
import tools_create_images as tci
import tools_voice_over as tvo
import tools_create_mp4 as tcm4
import tools_file_operations as tfo
import tools_query_openrouter as tqo
import tools_query_chatbot as tqc # Imported but not used in the consolidated functions
from flow_1_get_story_from_open_router import get_story_and_prompts # Explicitly import the function

# Define break_line for consistent use
break_line = "\n"

####################
# Create images
####################
def create_images(image_prompts, count_action_beats, xp_path, fn, error_list, image_files):
    # Default error image path
    image_error_path = os.path.join(os.path.dirname(__file__), "effects/1024p/cemetary_1024p.png") # Using relative path for robustness
    
    # Ensure the error image exists, otherwise use a placeholder or raise an error
    if not os.path.exists(image_error_path):
        # Fallback if the error image is not found
        image_error_path = "/tmp/default_error_image.png" # A temporary fallback
        if not os.path.exists(image_error_path):
            # If even the temporary fallback doesn't exist, we might need to create a dummy file or handle differently
            # For now, we'll assume it might be created or the user will ensure it exists.
            # A more robust solution would be to create a dummy image if none exists.
            pass 

    image_desc = []
    for i in range(1, count_action_beats + 1):
        print(f"Creating image for action beat {i}")

        # Use the image prompt directly from the generated list
        img_prompt = image_prompts[i-1] # image_prompts is 0-indexed

        print(break_line + "image prompt: " + str(i) + "\n" + img_prompt)

        # Construct path for the image file
        path_img_prefix = os.path.join(xp_path, fn + " - img")

        try:
            # Assuming tci.chatgpt_dalle takes the prompt, filename prefix, and index
            # The index '10 + i' seems arbitrary, might need clarification or adjustment
            image_url, filename = tci.chatgpt_dalle(prompt=img_prompt, fn=path_img_prefix, i=10 + i)
            image_files.append(filename)
        except Exception as e:
            print(f"Error creating image for prompt {i}: {e}")
            # User requested to just carry on if an image fails, without fallbacks.
            # The image_files list will only contain successfully created images.
            # error_list.append(f"Failed to create image for prompt {i}.") # Optionally add to error list

        image_desc.append(str(img_prompt))

    # Save the image descriptions to a file
    path_img_desc = os.path.join(xp_path, fn + " - image_desc" + ".txt")
    tfo.save_file(path_img_desc, str(image_desc)) # Use tfo.save_file


####################
# Create voice over
####################
def create_voice_over(story, gender, xp_path, fn):
    # Construct path for the audio file
    path_voice_prefix = os.path.join(xp_path, fn)
    model = "tts-1"  # or "tts-1-hd"
    
    # Determine voice based on gender
    if gender.lower() == "female":
        voice = "shimmer"
    else:
        voice = "onyx" # Default to male voice if not female
        
    print(f"Creating voice over with gender: {gender}, voice: {voice} for path: {path_voice_prefix}")
    
    # Create the audio file
    audio_file = tvo.text2mp3(text_string=story, model=model, voice_name=voice, fn=path_voice_prefix)
    
    return audio_file

##############################################
#### create mp4 - images and voice
##############################################
# image_files[]  -   image list for story
# story  - text for current story
# audiofile - current story voice over
# story_no -  current story no.
##############################################
def create_mp4(image_files, audio_file, xp_path, fn = ""):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Determine output MP4 filename
    if len(fn) < 2:
        output_mp4 = os.path.join(xp_path, str(current_time) + "story" + ".mp4")
    else:
        output_mp4 = os.path.join(xp_path, fn + ".mp4")
        
    print(f"Creating MP4: {output_mp4}")
    
    # Create the video using provided images and audio
    tcm4.create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)
    
    return output_mp4

##############################################
#### generate story MP4
##############################################
def generate_story_mp4(user_story_query, model="google/gemini-2.5-flash"):
    """
    Generates a story, creates images, voice-over, and compiles them into an MP4.

    Args:
        user_story_query (str): The user's input query for the story.
        model (str): The AI model to use for story generation.

    Returns:
        str or None: The path to the generated MP4 file, or None if generation failed.
    """
    
    # --- Story Type and Path Generation ---
    # Define a default query if the user input is too short
    if len(user_story_query) < 10:
        user_story_query = "I want a 700-1000 word sheriff or cop story of a very scary case or shift. NO supernatural stuff"

    # Determine the genre/story type using OpenRouter
    q_story_type = "u r a prof fiction writer. Figure out what story type the user is asking for. It can be 'ouija story', 'trucker story', 'sheriff story', 'cop story' ... or any type u think, but no more than 2 words. I want nothing but the story type as output - NO MORE THAN 2 WORDS. This is the user input: " + str(user_story_query)
    genre = tqo.query_openrouter(prompt=q_story_type, model=model)
    
    # Handle potential errors from OpenRouter
    if "Error querying OpenRouter" in genre:
        print(f"Warning: OpenRouter query failed for story type, using default genre. Error: {genre}")
        genre = "unknown_story"
    print(f"Determined Genre: {genre}")

    # Define the base path for YouTube content
    xp_path_base = '/Users/lasse/Desktop/my/youtube' # Base path for YouTube content
    
    # Create a dated folder for the story within the base path
    xp_path = tfo.create_dated_folder(xp_path_base, genre + "_story")
    print(f"Experiment path created: {xp_path}")
    os.makedirs(xp_path, exist_ok=True) # Ensure the directory exists

    # --- Story and Prompt Generation ---
    # Get the story, image prompts, gender, and filename prefix using the helper function
    # The get_story_and_prompts function handles the complex LLM interaction and data extraction
    story, image_prompts, gender, fn = get_story_and_prompts(user_story_query, model=model)

    # Check if essential data was generated
    if story is None or not image_prompts or gender is None or fn is None:
        print("Failed to generate story, image prompts, gender, or filename. Exiting MP4 generation.")
        return None # Return None to indicate failure

    # Extract the base filename without extension for use in subsequent functions
    fn_story = os.path.basename(fn)
    filename_without_extension, _ = os.path.splitext(fn_story)

    # --- Image Creation ---
    count_action_beats = len(image_prompts)
    image_files = [] # List to store paths of generated images
    error_list = []  # List to store any errors encountered during image creation

    # Call the function to create images based on the prompts
    create_images(image_prompts, count_action_beats, xp_path, filename_without_extension, error_list, image_files)

    # --- Voice Over Creation ---
    # Call the function to create a voice-over for the story
    audio_file = create_voice_over(story, gender, xp_path, filename_without_extension)

    # --- MP4 Creation ---
    # Call the function to create the final MP4 video
    output_final_mp4 = create_mp4(image_files, audio_file, xp_path, filename_without_extension)

    print(f"\nMP4 creation process finished.")
    print(f"Output MP4: {output_final_mp4}")
    
    # Report any errors that occurred during image creation
    if error_list:
        print("\nErrors encountered during image creation:")
        for error in error_list:
            print(f"- {error}")
            
    return output_final_mp4

# --- Main execution block ---
if __name__ == "__main__":
    # Example Usage:
    # You can modify these variables to test different story queries.
    
    # Example 1: Ouija Horror Story
    # user_story_query_example = "Disturbing True Ouija Horror"
    
    # Example 2: Cop Story
    user_story_query_example = "A scary story about a cop having a bad shift"
    
    # Example 3: Trucker Horror Story
    # user_story_query_example = "Disturbing True Ouija Horror"
    
    print(f"Starting story generation for query: '{user_story_query_example}'")
    
    # Call the main function to generate the story MP4
    mp4_path = generate_story_mp4(user_story_query_example)
    
    if mp4_path:
        print(f"\nSuccessfully generated MP4: {mp4_path}")
    else:
        print("\nFailed to generate MP4.")
