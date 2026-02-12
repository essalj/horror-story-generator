
import datetime
import os
import tools_create_images as tci
import tools_voice_over as tvo
import tools_create_mp4 as tcm4
import tools_file_operations as tfo
import tools_query_openrouter as tqo
from flow_1_get_story_from_open_router import get_story_and_prompts
import json # Added import for json
import tools_query_chatbot as tqc


break_line = "\n" # Define break_line

####################
# Create images
####################
def create_images(image_prompts, count_action_beats, xp_path, fn, error_list, image_files):
    image_error_path = "/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/cemetary_1024p.png"
    image_desc = []
    for i in range(1, count_action_beats + 1):
        print(f"Creating image for action beat {i}")

        # Use the image prompt directly from the generated list
        img_prompt = image_prompts[i-1] # image_prompts is 0-indexed

        print(break_line + "image prompt: " + str(i) + "\n" + img_prompt)

        path_img = os.path.join(xp_path, fn + " - img")

        try:
            # Assuming tci.chatgpt_dalle takes the prompt, filename prefix, and index
            image_url, filename = tci.chatgpt_dalle(prompt=img_prompt, fn=path_img, i=10 + i)
            image_files.append(filename)
        except Exception as e: # Catch specific exceptions if possible
            print(f"Error creating image for prompt {i}: {e}")
            if i > 1:
                image_files.append(image_files[-1]) # Reuse the former image
                error_list.append(f"Error creating image for prompt {i}, reused previous image.")
            else:
                image_files.append(image_error_path) # Use default error image
                error_list.append(f"Error creating image for prompt {i}, used default error image.")

        image_desc.append(str(img_prompt))

    path_img_desc = os.path.join(xp_path, fn + " - image_desc" + ".txt")
    tfo.save_file(path_img_desc, str(image_desc)) # Use tfo.save_file


####################
# Create voice over
####################
def create_voice_over(story, gender, xp_path, fn):
    path_voice = os.path.join(xp_path, fn )
    model = "tts-1"  #or "tts-1-hd"
    search_term = gender
    if search_term.lower()=="female":
        voice = "shimmer"
    else:
        voice = "onyx"
    print(f"Creating voice over with gender: {gender}, voice: {voice}", path_voice)
    tvo.text2mp3(text_string = story, model=model, voice_name = voice, fn=path_voice )
    audio_file = path_voice + ".mp3"
    return audio_file


##############################################
#### create mp4 - images and voice
# image_files[]  -   image list for story
# story  - text for current story
# audiofile - current story voice over
# story_no -  current story no.
#
##############################################
def create_mp4(image_files, audio_file, xp_path, fn = ""):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if len(fn)<2:
        output_mp4 = os.path.join(xp_path, str(current_time) + "story" + ".mp4")
    else: output_mp4 = os.path.join(xp_path, fn + ".mp4")
    print(f"Creating MP4: {output_mp4}")
    tcm4.create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)
    # Assuming count_words is a function you have elsewhere or can remove
    # count_words(story)
    return output_mp4


# writer_model = 'anthropic/claude-opus-4.6'
# writer_model = 'moonshotai/kimi-k2.5'
# writer_model='anthropic/claude-opus-4'
# Define necessary variables (these could be made into user inputs later)
# user_story_query ="A scary story about a cop having a bad shift"
def generate_story_mp4(user_query, model):
    # Ensure the experiment path exists
    print("writer model: " + model)
    break_line = "\n" # Define break_line

    # Get story details from user input
    if len(user_query)<5:
        user_query = "I want a scary ouija board story"

    # define genre
    # q_story_type = "u r a world class fiction writer. Figure out what story type the user is asking for. It can be 'ouija story', 'trucker story', 'sheriff story', 'cop story' ... or any type u think, but no more than 2 words. I want nothing but the story type as output - NO MORE THAN 2 WORDS. This is the user input: " + str(user_story_query)
    # genre = tqo.query_openrouter(prompt=q_story_type, model=writer_model)

    # if "Error querying OpenRouter" in genre:
    #     print(f"Warning: OpenRouter query failed, using default genre. Error: {genre}")
    #     genre = "probably_ouija_story"
    # print(genre)
    xp_path_0 = '/Users/lasse/Desktop/my/youtube' #mac

    xp_path = tfo.create_dated_folder(xp_path_0, genre + "_story")
    print("xp_path: " + str(xp_path))
    os.makedirs(xp_path, exist_ok=True)

    # 1. Get story text, image prompts, and gender
    # fn = file_path
    # story, image_prompts, gender, file_path, story_title
    
    # story, image_prompts, gender, fn, story_title = get_story_and_prompts(user_story_query, model=writer_model)
    # story, image_prompts, gender, story_title = get_story_and_prompts(user_query=user_story_query, model=writer_model)
    story, image_prompts, gender, story_title = get_story_and_prompts(user_query, model)
    if story is None or not image_prompts or gender is None:  # or fn is None:
        print("Failed to generate story, image prompts, gender, or filename. Exiting.")
        return None # Return None to indicate failure


    # fn_story = os.path.basename(fn)
    # filename_without_extension, _ = os.path.splitext(fn_story)
    fn_story = os.path.basename(story_title)
    filename_without_extension = fn_story
    
    # fn_story = os.path.basename(story_title)
    # fn_story = os.path.basename(fn)

    count_action_beats = len(image_prompts)
    image_files = []
    error_list = []

    # Call create_images with the generated prompts
    create_images(image_prompts, count_action_beats, xp_path, filename_without_extension, error_list, image_files)

    # Call create_voice_over with the generated story and gender
    audio_file = create_voice_over(story, gender, xp_path, filename_without_extension)

    # Call create_mp4 with the generated files
    output_final_mp4 = create_mp4(image_files, audio_file, xp_path, filename_without_extension)

    print(f"\nMP4 creation process finished.")
    print(f"Output MP4: {output_final_mp4}")
    if error_list:
        print("\nErrors encountered:")
        for error in error_list:
            print(f"- {error}")
    return output_final_mp4

# Define a default user_story_query for execution

if __name__ == "__main__" and 1==2:
    user_story_query = "A scary story about an ouija board game gone wrong"
    mp4_path = generate_story_mp4(user_story_query, writer_model)
    print(f"Generated MP4 path: {mp4_path}")



    