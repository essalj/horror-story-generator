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
action_beats_count = 5

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

    

#################
# create story
#################

story_no = 1
user_input = ""

# user_input = "A loyal dog saves the day but ends up dying from it"

# user_input = "Airbnb host is protagonist, guests are bad persons, a scam, the host manage to get well out of it"

if len(user_input)>5:
    user_input ="Build the plot based on these user_inputs:\n" + user_input + "." 
p_gender = "male"  # select male or female voice
if p_gender == "female":
    sel_voice = "shimmer"
else:
    sel_voice = "onyx"

main_task = open_file("task_AIRBNB.txt")
analysis = open_file("Airbnb story analysis.txt")
airbnb_stories = open_file("C:\\my\\__youtube\\videos\\Horror Stories - inspiration\\Airbnb stories - All.txt")
guide_lines = "\n - " + p_gender + ''' protagonist.\n - ALWAYS WRITE IN 1ST PERSON!'''


# 0b. Read the file Airbnb stories - All.txt
task_0 = main_task + '''
0. Read the analysis of Airbnb stories.
1. Create 5 ideas for a plot to a new True Airbnb horror story drawing inspiration from the analysis of airbnb stories.
''' + user_input + '''
   - For each plot idea outline the central conflict and resolution. This is the story's backbone, guiding the narrative direction.
   - insert the the full description in a new json stucture with the column 'plot idea'-
2. Take on the role as a critic and die hard fan of the genre and rate the 5 plot ideas on a scale from 1-100. 
   - **Rating: For each "plot idea" in the json structure assign a rating on a scale from 1 to 100. A score of 100 signifies that the story idea has potential as an exemplary piece of horror literature, perfectly marrying imaginative horror elements with a realistic setting that is very likely to be a true story, while a score of 1 indicates significant areas for improvement.
   - **Explain Your Rating**: Provide a detailed explanation for your rating, considering plot consistency, character depth, the effectiveness of the horror elements within a realistic framework, and the story’s overall ability to engage and horrify the reader.

  - For each "plot idea" from the existing json add your rating, an explanation for the rating and a rank from 1-5 to the existing json stucture with the columns ['rating', 'raters comment','rank'].
  3. The json structure should be as in this example:\n
  ```json
[
    {
        "plot idea": "The Counterfeit Vacation.
        An Airbnb host discovers his guests are using his property to create and distribute counterfeit currency.
        The host outsmarts the guests by gathering evidence and anonymously tipping off the authorities, leading to their arrest while he remains safe.",
        "rating": 78,
        "raters comment": "The idea of a scam unfolding within the confines of an Airbnb property is intriguing and has potential for psychological depth, but it may lack direct horror elements.",
        "rank": 3
    }
    ...
    ]
    ```
4. Output nothing but the created json structure. 
''' + break_line + '''
Airbnb analysis: ''' + analysis + break_line

task_1 = main_task + break_line + '''\n
1. From the json input select the plot idea with the highest rank. 
 - For the selected plot idea decide on key action beats.
    - Identify ''' + str(action_beats_count) + ''' pivotal moments that advance the plot. 
    - These action beats should highlight character development, escalate tension, and move the story towards its climax.
2. Based on your suggested plot develop a story template for an Airbnb horror story with ''' + str(action_beats_count) + ''' action beats.
   Follow these guidelines: \n''' + guide_lines + ''' 
3. Insert the story template into a new  json stucture with the column ['story_template"].
4. For each action beat create 1 image prompts that depicts the action.
5. Add the action beats and the image prompts in the json stucture ['action_beat_no.", 'action_beat_desc", "image_prompt"]
6. Create 1 image prompt that depicts the Airbnb residence and its settings and add it to the json structure with the column 
name ["first-image"].
7. Output nothing but the created json structure. ''' + break_line + '''\nJSON input:'''

# + '''
# Airbnb analysis: ''' + analysis + break_line + '''
# Airbnb stories:''' + airbnb_stories + break_line

task_2 = main_task + break_line + '''
1. Read the story template and the action beats from the json structure to understand the plot.
2. Write following these guide lines: ''' + guide_lines + '''
3. First develop the characters in depth.
  - Deepen character development by exploring their backstories, motivations, and fears more thoroughly to create a stronger emotional connection with the reader.
4. Write the intro of the Airbnb horror story. Make the intro peaceful and about the Airbnb residence.
 - Introduce foreshadowing elements early in the story to create anticipation and sow seeds of unease that will pay off during climactic moments.
 - Enhance the buildup of suspense by introducing more subtle and nuanced horror elements throughout the story, rather than relying on abrupt occurrences.
5. Continue with the action beats. Take them one by one and develop them in full detail describing back stories, consequences, details and emotions.
   Do not rush it, let the story unfold little by little. Remember we are aiming for 12000 words.
   Use "show - dont tell" methodology.
6. Write a detailed ending. Make it a good one - like a lucky escape, the bad person did not cone back, or something like that. 
But leave it open ended. And if you feel for it a little aftermath (a realisation after coming home, a letter, a call, a photo...
..or something entirely diferent).
7. Output nothing but the story.
\nJSON input:''' 
#suggets plot
def test_plot_ideas(task):  
    print(break_line + "story_plot")
    role = chatbot_role + task
    prompt = role
    print(break_line + "prompt: \n" + prompt)
    r = chatgpt3(prompt, model = gpt4)
    gpt_out = r.choices[0].message.content
    print(break_line + gpt_out)
    return gpt_out

def story_plot(task):  
    print(break_line + "story_plot")
    role = chatbot_role + task
    prompt = role
    print(break_line + "prompt: \n" + prompt)
    r = chatgpt3(prompt, model = gpt4)
    gpt_out = r.choices[0].message.content
    print(break_line + gpt_out)
    return gpt_out
# r1_json =story_plot(task_1)
# print(r1_json)

#write story
def write_story(task):  
    print(break_line + "story_plot")
    role = chatbot_role + task
    prompt = role
    print(break_line + "prompt: \n" + prompt)
    r = chatgpt3(prompt, model = gpt4)
    gpt_out = r.choices[0].message.content
    print(break_line + gpt_out)
    return gpt_out
 
# task_2_ = task_2 + r1_json
# # story = story_plot(task_2_)
# story = write_story(task_2_)
# count_words(story)
# path_story = os.path.join(xp_path, fn + " - story " + str(story_no) + ".txt")
# save_file(path_story, story)


#evaluate story
def evaluate_story(task):
    prompt = task
    r = chatgpt3(prompt, model = gpt4)
    gpt_out = r.choices[0].message.content
    return gpt_out

# task_3 = open_file("task_critic.txt") + "\n**Story:\n" + story + break_line + "**Current JSON Structure:\n" + r1_json
# r3_json = evaluate_story(task_3)
# print(r3_json)
r0_json = ""
r1_json = ""
r3_json = ""
story = ""
# def full_write_process():
# global r1_json, r3_json, story

# task 0
r0_json =test_plot_ideas(task=task_0)

# task 1
r1_json =story_plot(task_1 + r0_json)
print(r1_json)

# task 2
task_2_ = task_2 + r1_json
story = write_story(task_2_)
count_words(story)
path_story = os.path.join(xp_path, fn + " - story " + str(story_no) + ".txt")
save_file(path_story, story)

# task 3
task_3 = open_file("task_critic.txt") + "\n**Story:\n" + story + break_line + "**Current JSON Structure:\n" + r1_json
r3_json = evaluate_story(task_3)
print(r3_json)

# task_eval_stories = open_file("task_review_external_stories.txt") + "\nStories to review:\n" + break_line + airbnb_stories + break_line
# r4_json = evaluate_story(task_eval_stories)
# print(r4_json)

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



def create_first_image():
    user_txt = '''Select "first-image" from the json structure: \n
    json: \n''' + r1_json + '''\n
    Output only the content of "first-image. Output  it as a string'''
    first_image = json_extract(json=r1_json, user_prompt=user_txt)

    
    system_txt = chatbot_artist_role
    user_prompt = "Can you help me improve this image prompt to a world class illustration in a horror story:" + str(first_image) + "\nOutput only the improved image prompt."
    r = chatgpt3(userinput = user_prompt, system_role=system_txt, model = gpt4)
    img_prompt = r.choices[0].message.content
    print(break_line + "image prompt: \n" + img_prompt)

    #create image
    path_img = os.path.join(xp_path, fn + " - img")
    try:  #if no image or if problem with image then use another prompt
        image_url, filename = chatgpt_dalle(prompt = img_prompt, fn= path_img, i=0)
        image_files.append(filename)
    except:
        image_url, filename = chatgpt_dalle(prompt = "A beautiful yet scary looking Airbnb rental.", fn= path_img, i=nc + j)
        image_files.append(filename)


def images_for_story(json_, story_no):
    images_pr_chapter = action_beats_count
    image_path = []
    nc = (story_no)*10
        
    for j in range(1, 1 + images_pr_chapter):
        print(j)
        system_txt = chatbot_artist_role

        user_txt = '''Select "image_prompt" from the json structure where "action_beat_no." = ''' + str(j) + ''': \n
        json: \n''' + json_+ '''\n
        Improve the selected image prompt.'''
        # Output only the selected image prompt.'''
        # print(user_txt)

        r = chatgpt3 (userinput = user_txt, system_role=system_txt, model = gpt4)
        img_prompt = r.choices[0].message.content
        print(break_line + "image prompt: \n" + img_prompt)

        rephrase_txt = '''If you get an error from Dall-e related to content policy or something else when creating an image
        then rephrase the prompt and try again!
        '''
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


image_files = []
create_first_image()
image_files = images_for_story(json_=r1_json, story_no=story_no)

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
