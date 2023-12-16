#pip install Pillow

import re
import os
import openai
from openai import OpenAI
from time import time,sleep
import datetime


def create_dated_folder(base_path, text_add_on):
    # Get today's date in yyyy-mm-dd format
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    folder_name = f"{today_date}_{text_add_on}"

    # Create the full path for the new folder
    new_folder_path = os.path.join(base_path, folder_name)

    # Create the folder
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder created: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")
    return new_folder_path
    # Create folder
    #xp_path = "C:\\my\\__youtube\\videos"
    #additional_text = "horror"  # Replace with your desired text
    #create_dated_folder(xp_path, additional_text)


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
    # Regex pattern to match disallowed characters
    pattern = r'[\\/:*?"<>|]'
    # Replace disallowed characters with an empty string
    return re.sub(pattern, '', filename)


#############################
## Create folder for export
cwd_path = os.getcwd()
xp_path_0 = "C:\\my\\__youtube\\videos"
additional_text = "horror"  # Replace with your desired text
xp_path = create_dated_folder(xp_path_0, additional_text)

openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
# openai_api_key = userdata.get('openai')
client = OpenAI(api_key=openai_api_key)

# openai.api_key = open_file('openaiapikey.txt')
chapters = [ '1', '2', '3', '4', '5', '6', '7']

chatbot_role = open_file("chatbot_role.txt")
task = open_file("task.txt")

# models
# model = "gpt-4-1106-preview"
# model = "gpt-3.5-turbo-1106"
def chatgpt3 (userinput, temperature=0.8, frequency_penalty=0.2, presence_penalty=0, system_role=chatbot_role):
    messagein = [
        {"role": "user", "content": userinput },
        {"role": "system", "content": system_role}]
    # response = openai.ChatCompletion.create(
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messagein
    )
    text = response.choices[0].message.content
    return response
#####################################

#######################
#### Shape user input
chatbot_role = open_file("chatbot_role.txt")
task = open_file("task.txt")
break_line = "\n" + 50*"-" + "\n"

user_input = ""
user_input = "Cinderella as a horror story, BUT CHANGE THE NAME TO SOMETHING ALKE"

# user_input = "A very scary horror story about an AI girlfriend using its owner to rake profit to its creator. Do not name the AI after known AI's. It is a psycological scary story, NO HAPPY END and NO FRIENDSHIPS!!"

role = chatbot_role + task
prompt = role + "\nEvaluate this user input for a scary horror story and develop it into a story idea and template for a 7 page story: " + user_input + ".\nIf there is no user input then create it based on randomly selecting a time in history or future, a well known destination and an out of the ordinary protagonist and then develop the story idea"
r = chatgpt3(prompt)
story_idea = r.choices[0].message.content
print(break_line + "\n" + story_idea + break_line)


###############
#   WRITING   #
###############
######################################
#### create title and a named folder 
role = chatbot_role + task
idea = story_idea
task1 = "\nCreate 5 innovative SEO optimized very catchy and intriguing titles that will attract viewers, for a story based on the story idea below: \n"
task2 = "\nCreate 5 innovative SEO optimized super catchy titles for a story based on the story idea above."
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
print("Titles" + break_line + prompt)
r = chatgpt3(prompt)
titles = r.choices[0].message.content
print(titles)


prompt = "Read the suggestions and pick the one you think attracts most audience" + titles + "\n\nReturn nothing but the title"
r = chatgpt3(prompt)
title = r.choices[0].message.content
fn = sanitize_filename(title)
print(break_line + title)
print(fn + break_line)  



################################
## Story comments by critic
idea = story_idea
role = chatbot_role + task
task1 = "Read through the draft below with a critics eyes and comment in order to help the writer make the story world class."
task2 = "Read through the draft above with a critics eyes and comment in order to help the writer make the story world class."
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(prompt)
critic = r.choices[0].message.content
print("Critics notes")
print(break_line)
print(prompt)
print(critic)
print(break_line)


#######################################
## Implement story comments by critic
idea = "Draft story: " + story_idea + break_line + "\nCritics comments:" + critic
role = chatbot_role + task
task1 = "Read through the draft story and the critic notes below. Use the critics comments to improve the draft."
task2 = "Read through the draft story and the critic notes above. Use the critics comments to improve the draft."
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(prompt)
improved_draft = r.choices[0].message.content

print("\n\nImproved_draft")
print(break_line)
print(prompt)
print(improved_draft)
count_words(improved_draft)
print(break_line)



#Build the critic comments outlines - story line on 7 chapters
idea = improved_draft
role = chatbot_role + task
task1 = "Write a 7 chapter detailed outline for the horror story named '" + title + "' based on the following draft story. Make it very detailed and explicit so the story can be written from that as sole input:"
task2 = "Write a 7 chapter detailed outline for the horror story named '" + title + "' based on the draft story above. Make it very detailed and explicit so the story can be written from that as sole input. REMEMBER I WANT EXACTLY 7 CHAPTERS!!!!"
outline2 = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(outline2)
outline3 = r.choices[0].message.content

print("\n\nOutline Chapters")
print(break_line)
print(prompt)
print(outline3)

path_outline = os.path.join(cwd_path, "outline.txt")
save_file(path_outline, outline3)
count_words(outline3)
print(break_line)



#######################
## Write the chapters
idea = outline3
role = chatbot_role + task
task1 = "Read all the chapter outlines below in order to get the right context. Then WRITE CHAPTER <<NUM>> ONLY!!! Write in great detail and in a vivid and intriguing language from the following information."
task2 = "Read all the chapter outlines above in order to get the right context. Then WRITE CHAPTER <<NUM>> ONLY. WRITE IN GREAT DETAIL AND IN A VIVID AND INTRIGUING LANGUAGE FROM THE INFORMATION ABOVE. Make sure you only write words meant to be in the final story, so no editorial notes etc.!!"
write_chapter = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
print("\n\nChapters")
print(break_line)
print(prompt)
print(write_chapter)

chapters_ = []
for chapter in chapters:
    # chap = outline3
    # chap = open_file("chapters.txt")
    # wchapter = open_file("write_chapters.txt").replace("<<ROLE>>", role).replace("<<NUM>>", chapter).replace("<<CHAP>>", chap)
    wchapter = write_chapter.replace("<<NUM>>", chapter)
    r = chatgpt3(wchapter)
    wchapter2 = r.choices[0].message.content
    chapters_.append(wchapter2)
    print(wchapter2)

story = "\n".join(chapters_)
path_story = os.path.join(xp_path, fn + " - story.txt")
save_file(path_story, story)
count_words(story)
print(break_line)


################
## description
idea = story_idea
role = chatbot_role + task
task1 = "Create a seo and youtube search optimized description to the youtube horror story descibed in the summaries below. Do not list the chapters. Use mark down and emojies.\n" 
task2 = "Create a seo and youtube search optimized description to the youtube horror story descibed in the summaries above. Do not list the chapters. Use mark down and emojies." 
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(prompt)
desc = r.choices[0].message.content
path_ = os.path.join(xp_path, fn + " - desc.txt")
save_file(path_, desc)
print("\n\nDescription")
print(break_line)
print(prompt)
print(desc)
print(break_line)


###########
## thanks
system_txt = "You are a Horror story writer."
user_txt = "The audience has just listened to the horror story descibed here: " + str(story_idea) + ". /nCreate a thank you for listening greeting and remind audience to like and subscribe"
r = chatgpt3(system_txt + user_txt)
thanks = r.choices[0].message.content
path_ = os.path.join(xp_path, fn + " - thanks.txt")
save_file(path_, thanks)
print(break_line)
print("Thanks")
print(prompt)
print("\n-----------------\n", thanks)
print(break_line)


###################
###################
#   create pics   #
###################
import requests
from PIL import Image
from io import BytesIO


#Dalle3
def chatgpt_dalle(prompt="A white siamese cat balancing on a sign saying TEST", fn="image", i=1):
    # Presuming `client.images.generate` is a valid method call for the API client you're using
    # response = openai.Image.create(
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
    filename = f"{fn}{i}.png"
    image.save(filename)

    # Return the image URL and the path to the saved image file
    return image_url, filename
#image_url, filename = chatgpt_dalle("a blue cat", fn="my_cat_image_", i=42)


images_pr_chapter = 2
for n,c in enumerate(chapters_):
    nc = (n*10)
    
    for j in range(1, 1 + images_pr_chapter):
        print(j)
        img_prompt = '''You are an experienced youtube artist. Can you help me create a scary picture for this chapter in a horror story. 
        Make sure the image is dark and haunting, but unresistable. 
        DO NOT PUT TEXT ON THE IMAGE!!!. 
        If you get  an error when creating an image then rephrase and try again!
        --------------
        End the prompt with the keywords: 4k, cinematic, b/w, photorealistic, very scary. 
        Description: \n''' + c
        path_img = os.path.join(xp_path, fn + " - img")
        image_url, filename = chatgpt_dalle(prompt = img_prompt, fn= path_img, i=nc + j)

  
# create images for youtube thumbnail
ytn_prompt = '''You are an experienced youtube artist. Can you help me create a thumbnail for my channel for a horror story. The horror story is described in this story board. Make sure the image is dark and haunting, but unresistable - so the audience cannot help them selves. Do not add any text to the picture. End the prompt with the keywords: 4k, cinematic, b/w, photorealistic, very scary. \n\nDescription: \n''' + desc
path_img = os.path.join(xp_path, fn + " - ytmb")
image_url, filename = chatgpt_dalle(prompt = ytn_prompt, fn= path_img, i=9999)



##################
#   VOICE OVER   #
##################

#tt = story
# scenes = tt.split("-----")

# tts-1 is optimized for real-time use cases and tts-1-hd is optimized for
# https://platform.openai.com/docs/guides/text-to-speech/voice-options - 6 preset voices (preferred grandmother = Shimmer, preferred male reader = Echo)
def text2mp3(text_string = "testing", voice_name = "onyx", fn = fn):
  speech_file_path = fn + ".mp3"
  response = client.audio.speech.create(
    model = "tts-1",
    voice = "shimmer",
    input = text_string
  )
  response.stream_to_file(speech_file_path)
# text2mp3(text_string = tt, voice_name = "shimmer", fn="Lullaby")

# create voice for chapters
for n,c in enumerate(chapters_):
    nc = n + 1
    path_voice = os.path.join(xp_path, fn + " - audio_" + str(nc))
    print(path_voice)
    text2mp3(text_string = c, voice_name = "echo", fn=path_voice)


#voice - thanks
path_voice = os.path.join(xp_path, fn + " - thanks - audio_99")
text2mp3(text_string = thanks, voice_name = "onyx", fn=path_voice )




#################
## Create mp4
# from create_mp4 import * 
from create_mp4 import *

# xp_path = 'C:\\my\\__youtube\\videos\\2023-12-13_horror'
#List all files in the specified directory ending with ...
def get_file_names(directory, pattern = ".mp3"):
    files = os.listdir(directory)
    l_files = [file for file in files if file.endswith(pattern)]
    return l_files

#directory_path = xp_path  #'/path/to/directory'  # Replace with your directory path
audio_files = get_file_names(directory = xp_path, pattern = ".mp3")
image_files = get_file_names(directory = xp_path, pattern = ".png")

audio_count = len(audio_files)
image_count = len(image_files)


mp4_clips = []
# joins images and audio on audio file level
for n,c in enumerate(audio_files):
    images_pr_audio_clip = 2
    img_base_no = n * images_pr_audio_clip
    output_mp4 = os.path.join(xp_path, "clip_" + str(n) + ".mp4")
    mp4_clips.append(output_mp4)
    try: # handles if we run out of pictures
        image_paths = [os.path.join(xp_path, image_files[img_base_no]), os.path.join(xp_path, image_files[img_base_no+1])] 
        # image_path = os.path.join(xp_path, image_files[n])
    except:
        image_paths = os.path.join(xp_path, image_files[-1])
        
    audio_path = os.path.join(xp_path, audio_files[n])
    print(audio_path, " x ", image_paths, " = ", output_mp4)

    create_video_with_images_and_audio(image_paths=image_paths, audio_path=audio_path, output_filename=output_mp4, fps=30)

    # create_video_with_images_and_audio(xp_path=xp_path, image_path, audio_path, output_filename=output_mp4, fps=30)
        # create_video_with_audio(xp_path=xp_path, image_path = image_path, audio_path = audio_path, output_filename=output_mp4, fps=30, silence_duration = 2)
    # create_video_with_audio(image_path = image_path, audio_path = audio_path, output_filename=output_mp4, fps=30, silence_duration = 2)

 
#joins  all mp4 clipsaudio_files = get_file_names(directory = xp_path, pattern = ".mp3")
output_final_mp4 = os.path.join(xp_path, "final_mp4.mp4")

path0 = os.getcwd()
os.chdir(xp_path) # exec in xport library
concatenate_videos(mp4_clips, output_final_mp4)
os.chdir(xp_path)


###########################
# Adding music sound track
###########################

