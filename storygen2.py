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
os.getcwd()

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
chatbot = open_file("chatbot_role.txt")
chapters = [ '1', '2', '3', '4', '5', '6', '7']

# models
# model = "gpt-4-1106-preview"
# model = "gpt-3.5-turbo-1106"
def chatgpt3 (userinput, temperature=0.8, frequency_penalty=0.2, presence_penalty=0):
    messagein = [
        {"role": "user", "content": userinput },
        {"role": "system", "content": chatbot}]
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
user_input = "A very scary horror story about an AI girlfriend using its owner to rake profit to its creator. Do not name the AI after known AI's. It is a psycological scary story, NO HAPPY END and NO FRIENDSHIPS!!"
#role = open_file("chatbot_role.txt")
prompt = "You are a horror writer. Evaluate this user input to a scary horror story  and refine it, but do not write the story. This is just inspirational notes" + user_input
r = chatgpt3(prompt)
user_input = r.choices[0].message.content
print(user_input)



###############
#   WRITING   #
###############

######################################
#### create title and a named folder 
role = open_file("chatbot_role.txt")
idea = user_input
task1 = "Create 5 innovative SEO optimized super catchy titles that are bound to lure the viewer in, for a story based on the users input below: \n"
task2 = "\nCreate 5 innovative SEO optimized super catchy titles for a story based on the users input above."
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
print(prompt)
r = chatgpt3(prompt)
titles = r.choices[0].message.content
print(titles)


prompt = "Read the suggestions and pick the one you think attracts most audience" + titles + "\n\nReturn nothing but the title"
r = chatgpt3(prompt)
title = r.choices[0].message.content
fn = sanitize_filename(title)
print(title)
print(fn)  


###################
#### Draft story
idea = user_input
role = open_file("chatbot_role.txt")
task1 = "Write a draft to a horror story named '" + title + "'. Base it on users input below."
task2 = "Write a draft to a horror story named '" +  title +"'. Base it on users input above."
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(prompt)
draftX = r.choices[0].message.content
print(prompt)
print(draftX)
count_words(draftX)


################################
## Story comments by critic
idea = draftX
role = open_file("chatbot_role.txt")
task1 = "Read through the draft below with a critics eyes in order to make the story world class and comment."
task2 = "Read through the draft above with a critics eyes in order to make the story world class and comment."
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(prompt)
critic = r.choices[0].message.content
print(prompt)
print(critic)


#######################################
## Implement story comments by critic
idea = "Draft story: " + draftX + "\nCritics comments:" + critic
role = open_file("chatbot_role.txt")
task1 = "Read through the draft story and the critic notes below. Use the critics comments to improve the draft."
task2 = "Read through the draft story and the critic notes above. Use the critics comments to improve the draft."
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(prompt)
improved_draft = r.choices[0].message.content
print(prompt)
print(improved_draft)
count_words(improved_draft)



#Build the critic comments outlines - story line on 7 chapters
idea = improved_draft
role = open_file("chatbot_role.txt")
task1 = "Write a 7 chapter detailed outline for the horror story named '" + title + "' based on the following draft:"
task1 = "Write a 7 chapter detailed outline for the horror story named '" + title + "' based on the draft above"
outline2 = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(outline2)
outline3 = r.choices[0].message.content
print(prompt)
print(outline3)

path_outline = os.path.join(cwd_path, "outline.txt")
save_file(path_outline, outline3)
count_words(outline3)


#######################
## Write the chapters
idea = outline3
role = open_file("chatbot_role.txt")
task1 = "Write Chapter <<NUM>> only!!! Write in great detail and in a vivid and intriguing language from the following information."
task2 = "WRITE CHAPTER <<NUM>> ONLY. WRITE IN GREAT DETAIL AND IN A VIVID AND INTRIGUING LANGUAGE FROM THE INFORMATION ABOVE. Make sure you only write words meant to be in the final story, so no editorial notes etc.!!"
write_chapter = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
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


################
## description
idea = draftX
role = open_file("chatbot_role.txt")
task1 = "Create a seo optimized description to the youtube horror story descibed in the summaries below. Do not list the chapters. Use mark down and emojies.\n" 
task2 = "Create a seo optimized description to the youtube horror story descibed in the summaries above. Do not list the chapters. Use mark down and emojies." 
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(prompt)
desc = r.choices[0].message.content
path_ = os.path.join(xp_path, fn + " - desc.txt")
save_file(path_, desc)
print(prompt)
print("\n-----------------\n", desc)


###########
## thanks
system_txt = "You are a Horror story writer."
user_txt = "The audience has just listened to the horror story descibed here: " + str(draftX) + ". /nCreate a thank you for listening greeting and remind audience to like and subscribe"
r = chatgpt3(system_txt + user_txt)
thanks = r.choices[0].message.content
path_ = os.path.join(xp_path, fn + " - thanks.txt")
save_file(path_, thanks)
print(prompt)
print("\n-----------------\n", thanks)



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


for n,c in enumerate(chapters_):
    nc = n + 1
    
    img_prompt = '''You are an experienced youtube artist. Can you help me create a scary picture for a this chapter in a horror story. \nMake sure the image is dark and haunting, but unresistable - so the audience cannot help them selves. Do not add any text to the picture. \n--------------\nEnd the prompt with the keywords: 4k, cinematic, b/w, photorealistic, very scary. \n\nDescription: \n''' + c
    path_img = os.path.join(xp_path, fn + " - img")
    image_url, filename = chatgpt_dalle(prompt = img_prompt, fn= path_img, i=nc)

  
# create images for youtube thumbnail
ytn_prompt = '''You are an experienced youtube artist. Can you help me create a thumbnail for my youtube channel for a horror story. The horror story is described in this story board. Make sure the image is dark and haunting, but unresistable - so the audience cannot help them selves. Do not add any text to the picture. End the prompt with the keywords: 4k, cinematic, b/w, photorealistic, very scary. \n\nDescription: \n''' + desc
path_img = os.path.join(xp_path, fn + " - ytmb")
image_url, filename = chatgpt_dalle(prompt = ytn_prompt, fn= path_img, i=1)



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
    text2mp3(text_string = c, voice_name = "shimmer", fn=path_voice)


#voice - thanks
path_voice = os.path.join(xp_path, fn + " - thanks - audio_99")
text2mp3(text_string = thanks, voice_name = "onyx", fn=path_voice )




#################
## Create mp4
# from create_mp4 import * 
import create_mp4
# import os
# os.getcwd()