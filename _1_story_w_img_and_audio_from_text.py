#pip install Pillow
# pip install pydub
import re
import os
import openai
from openai import OpenAI
from time import time,sleep
import datetime


def create_dated_folder(base_path, text_add_on):
    # Get today's date in yyyy-mm-dd format
    # today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # datetime_string = now.strftime("%Y%m%d_%H%M")
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    folder_name = f"{datetime_string}_{text_add_on}"

    # Create the full path for the new folder
    new_folder_path = os.path.join(base_path, folder_name)

    # Create the folder
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder created: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")
    return new_folder_path


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
        

def count_words(my_string):
  words = re.findall(r'\b\w+\b', my_string)
  number_of_words = len(words)
  print("Number of words:", number_of_words)


def sanitize_filename(filename):
    pattern = r'[\\/:*?"<>|]'     # Regex pattern to match disallowed characters
    return re.sub(pattern, '', filename)      # Replace disallowed characters with an empty string



#############################
## Create folder for export
#############################
# Create folder
cwd_path = os.getcwd()
xp_path_0 = "C:\\my\\__youtube\\videos"
additional_text = "horror"  # Replace with your desired text
xp_path = create_dated_folder(xp_path_0, additional_text)


# Get key for openai
# openai_api_key = userdata.get('openai')
# openai.api_key = open_file('openaiapikey.txt')
openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)



###############
# Definitions
###############
fn = "AirBNB stories"  #file name
# chapter_count = 3 # number of stories
action_beats_count = 6
break_line = "\n" + 50*"-" + "\n"

chatbot_role = open_file("chatbot_role.txt")
chatbot_artist_role = open_file("chatbot_artist_role.txt")

break_line = "\n" + 50*"-" + "\n"

# models
gpt4 = "gpt-4-1106-preview"
gpt3 = "gpt-3.5-turbo-1106"

#chatbot
def chatgpt3 (userinput, temperature=0.8, frequency_penalty=0.2, presence_penalty=0, system_role=chatbot_role, model = gpt3):
    messagein = [
        {"role": "user", "content": userinput },
        {"role": "system", "content": system_role}]
    response = client.chat.completions.create(
        model = model,
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messagein
    )
    text = response.choices[0].message.content
    return response
#####################################

#################
# tools
#######
#extracts text elements from json structure
def json_extract(json, user_prompt):
    # system_txt = chatbot_artist_role
    system_txt = "You are a helpful data scientist."
    r = chatgpt3(userinput = user_prompt, system_role=system_txt, model = gpt4)
    json_extract = r.choices[0].message.content
    print(break_line + "json extract: \n" + json_extract)
    return json_extract


def json_extract_keyword(json, keyword):
    user_prompt = "Select '" + keyword + "' from the json structure: \n" + json + "\nOutput only the content of '"  + keyword + "'. Output it as a string."
    system_txt = "You are a helpful data scientist."
    r = chatgpt3(userinput = user_prompt, system_role=system_txt, model = gpt4)
    json_extract = r.choices[0].message.content
    print(break_line + "json extract: \n" + json_extract)
    return json_extract
    #proposed_action = json_extract_keyword(json=r3_json, keyword="proposed action")

##############
# Read story
##############
story_no = 1
sel_voice = "onyx"   # "shimmer"=female "onyx"=male
story = open_file("gpt_story 2.txt") 

path_story = os.path.join(xp_path, fn + " - story " + str(story_no) + ".txt")
save_file(path_story, story)

task_img_prompts_from_story = '''
1. Read the story.
2. create an image prompt describing in positive phrases the Airbnb residence.
3. Insert it in a new json structure with the coloumn names ["image_no", "image_prompt"]. Assign it to "image_no" 0.
4. Break down the full story into scenes and create an image prompt describing each scene. 
5. Numerate them in "image_no" starting with 1 and insert the image prompts in the existing json structure with the 
coloumn names ["image_no", "image_prompt"]
6. Output nothing but the json structure.
\nStory:\n
''' + story


def story_2_image_prompt(task):  
    print(break_line + "story_2_image_prompt")
    prompt = chatbot_artist_role + task
    print(break_line + "prompt: \n" + prompt)
    r = chatgpt3(prompt, model = gpt4)
    gpt_out = r.choices[0].message.content
    print(break_line + gpt_out)
    return gpt_out

json_images = story_2_image_prompt(task_img_prompts_from_story)
print(json_images)

###################
###################
#   create pics   #
###################
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime


#Dalle3 - create image
def chatgpt_dalle(prompt="A white siamese cat balancing on a sign saying TEST", fn="image", i=1):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="standard",
        n=1,
    )
    # Get the image URL from the response
    image_url = response.data[0].url

    # Use requests to get the image from the URL
    image_response = requests.get(image_url)

    # Open the image and save it
    image = Image.open(BytesIO(image_response.content))

    # Get current date and time
    now = datetime.now()
    datetime_string = now.strftime("%Y%m%d_%H%M%S")
    filename = f"{fn}{i}_{datetime_string}.png"
    image.save(filename)
    print("save(filename): " + str(filename))
    # Return the image URL and the path to the saved image file
    return image_url, filename
#image_url, filename = chatgpt_dalle("a blue cat", fn="my_cat_image_", i=42)




def images_for_story(json_):
    images_pr_chapter = action_beats_count
    image_path = []
    nc = 10

    user_txt = "What is the highest 'image_no' in this json? Return nothing but the number. \nJson:\n" + json_
    r = chatgpt3 (userinput = user_txt, system_role="You are a data analyst.", model = gpt4)
    image_no_max = int(r.choices[0].message.content)
    print(image_no_max)    
    
    for j in range(0, image_no_max):
        user_txt = '''
        1. Select "image_prompt" from the json structure where "image_no" = ''' + str(j) + '''
        2. Improve the selected image prompt.
          - If there is no match on "image_no" then return "none"
        \nJson: \n''' + json_

        r = chatgpt3 (userinput = user_txt, system_role=chatbot_artist_role, model = gpt4)
        img_prompt = r.choices[0].message.content
        print(break_line + "image prompt: \n" + img_prompt)

        rephrase_txt = '''If you get an error from Dall-e related to content policy or something else when creating an image
        then rephrase the prompt and try again!
        '''

        print(str(j) + ". " + img_prompt)
        dalle_prompt = img_prompt + break_line + rephrase_txt
        print(break_line + dalle_prompt)

        try:
            path_img = os.path.join(xp_path, fn + " - img")
        except:
            path_img = image_path[j - 1]
        image_path.append(path_img)
        
        try:  #if no image or if problem with image then reuse the former
            image_url, filename = chatgpt_dalle(prompt = img_prompt, fn= path_img, i=nc + j)
            image_files.append(filename)
        except:
            image_files.append(image_files[-1])

    return image_files
# images_for_story(json_images)

image_files = []
image_files = images_for_story(json_=json_images)

# print(r1_json)

##################
#   VOICE OVER   #
##################
import os
from moviepy.editor import AudioFileClip, concatenate_audioclips

def split_text(text, max_length=4096):
    """
    Splits the text into chunks, each of maximum length `max_length`.
    Tries to split at sentence ends for natural sounding speech.
    """
    words = text.split()
    current_chunk = []
    for word in words:
        if len(' '.join(current_chunk + [word])) > max_length:
            yield ' '.join(current_chunk)
            current_chunk = [word]
        else:
            current_chunk.append(word)
    yield ' '.join(current_chunk)
from moviepy.editor import AudioFileClip, concatenate_audioclips


def text2mp3(text_string="testing", voice_name="onyx", fn="output"):
    text_string = "   " + text_string
    if len(text_string) <= 4096:
        # Process the entire text if it's shorter than 4096 characters
        speech_file_path = f"{fn}.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice_name,
            input=text_string
        )
        response.stream_to_file(speech_file_path)
    else:
        # Split and process the text in chunks
        audio_clips = []
        temp_files = []
        for index, text_chunk in enumerate(split_text(text_string)):
            speech_file_path = f"{fn}_{index}.mp3"
            temp_files.append(speech_file_path)
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice_name,
                input=text_chunk
            )
            response.stream_to_file(speech_file_path)
            audio_clip = AudioFileClip(speech_file_path)
            audio_clips.append(audio_clip)

        # Concatenate audio clips
        concatenated_audio = concatenate_audioclips(audio_clips)
        concatenated_audio.write_audiofile(fn + ".mp3")

        # Close the clips and delete temporary files
        for clip in audio_clips:
            clip.close()

        for file_path in temp_files:
            os.remove(file_path)
# Example usage
# text2mp3(text_string="Your long text here...", voice_name="shimmer", fn="Lullaby")

# story = open_file('gpt_story.txt')
# sel_voice = "onyx"   # "shimmer"
path_voice = os.path.join(xp_path, fn + " - " + str(story_no))
text2mp3(text_string = story, voice_name = sel_voice, fn=path_voice )
audio_file = path_voice + ".mp3"
count_words(story)




#### create mp4 - images and voice
# image_files[]  -   image list for story
# story  - text for current story
# audiofile - current story voice over
# story_no -  current story no.
#   
##############################################
from tools_create_mp4_delete import *

output_mp4 = os.path.join(xp_path, "clip_" + str(story_no) + ".mp4")
create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)
count_words(story)


#joins  all mp4 
# clipsaudio_files = get_file_names(directory = xp_path, pattern = ".mp3")
# xp_path = 'C:\\my\\__youtube\\videos\\2023-12-16_horror'
output_final_mp4 = os.path.join(xp_path, "concat_clips_mp4.mp4")

path0 = os.getcwd()
os.chdir(xp_path) # exec in xport library
concatenate_videos(mp4_clips, output_final_mp4)
os.chdir(path0)



###########################
# Adding music sound track
###########################
from tools_add_music_to_mp4 import * 

output_final_mp4 = output_mp4
output_final_mp4_music = os.path.join(xp_path,fn + "final_mp4_music.mp4")
add_ambient_music_to_video(
    video_file_path=output_final_mp4,
    music_folder_path='C:\\my\\__youtube\\videos\\horror_music',
    output_file_path=output_final_mp4_music,
    music_volume=0.03  # Adjust volume as needed
    )


# Add playlist and thanks too music artists
playlist = ['Frightmare - Jimena Contreras - Copy.mp3', 'Kirwani - Teental - Aditya Verma, Subir Dev - Copy.mp3', "Devil's Organ - Jimena Contreras - Copy.mp3", 'Funeral in Sinaloa - Jimena Contreras - Copy.mp3', 'Mayan Ritual - Jimena Contreras - Copy.mp3']

# Open the file in append mode
with open(path_desc, 'a') as file:
    # Write a thank you note
    file.write("\n\nA million thanks to the talented artists for creating this wonderfully intense music. \nHere is the playlist:\n")

    # Add each song from the playlist
    for song in playlist:
        t = song.replace('- Copy.mp3','')
        # print(t)
        file.write(f"- {t}\n")

# The file is automatically saved and closed when exiting the 'with' block
