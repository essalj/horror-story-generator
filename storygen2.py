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


# Create folder for export
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

# def chatgpt3(system_prompt, text_prompt, model="gpt-3.5-turbo-1106"):
#   response = client.chat.completions.create(
#     model = model,
#     messages=[
#       {"role": "system", "content": system_prompt},
#       {"role": "user", "content": text_prompt}
#     ]
#   )
#   return response

###############
#   WRITING   #
###############
#if __name__ == '__main__':
#Build the story idea
idea = open_file("user_input.txt")
role = open_file("chatbot_role.txt")
task1 = "Write a draft to a horror story based on users input:"
task2 = "If there is no user input you pick an interesting and surprisiing theme for the horror story."
draft2 = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(draft2)
draft3 = r.choices[0].message.content
print(draft3)

path_draft = os.path.join(cwd_path, "draft.txt")
save_file(path_draft, draft3)
count_words(draft3)



#Build the story outlines - story line on 7 chapters
idea = open_file(path_draft)
role = open_file("chatbot_role.txt")
task1 = "Write a 7 chapter detailed outline for the story from the following draft:"
task2 = "Write a 7 chapter detailed outline for the story from the draft above"
outline2 = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(outline2)
outline3 = r.choices[0].message.content
print(outline3)

path_outline = os.path.join(cwd_path, "outline.txt")
save_file(path_outline, outline3)
count_words(outline3)



# Chapter improvement by critic
idea = open_file(path_outline)
role = open_file("chatbot_role.txt")
task1 = "Read through the 7 chapter outlines below with a critics eyes and improve them:"
task2 = "Read through the 7 chapter outlines above with a critics eyes and improve them:"
chapter2 = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
r = chatgpt3(chapter2)
chapter3 = r.choices[0].message.content
print(chapter3)

path_chapters = os.path.join(cwd_path, "chapters.txt")
save_file(path_chapters, chapter3)
count_words(chapter3)


# create title and a folder name
r = chatgpt3("What is a good title of the following story outline. : " + chapter3 + "\nReturn nothing but the title")
title = r.choices[0].message.content
forbidden_chars = '/:*?"<>|'
fn = ''.join(char for char in title if char not in forbidden_chars)
print(fn + " ; " + title)




#Write the chapters
chapters_ = []
for chapter in chapters:
    chap = open_file("chapters.txt")
    wchapter = open_file("write_chapters.txt").replace("<<ROLE>>", role).replace("<<NUM>>", chapter).replace("<<CHAP>>", chap)
    r = chatgpt3(wchapter)
    wchapter2 = r.choices[0].message.content
    chapters_.append(wchapter2)
    print(wchapter2)

story = "\n".join(chapters_)
path_story = os.path.join(xp_path, fn + " - story.txt")
save_file(path_story, story)
count_words(story)


#description
system_txt = "You are a Horror story writer."
task1 = "\nCreate a seo optimized description to the youtube horror story descibed in the summaries below. Do not list the chapters. Use mark down and emojies.\n" 
idea = str(chapter3)
task2 = "\n---------------\nCreate a seo optimized description to the youtube horror story descibed in the summaries above. Do not list the chapters. Use mark down and emojies." 
prompt = system_txt + task1 + idea + task2
r = chatgpt3(prompt)
desc = r.choices[0].message.content
path_ = os.path.join(xp_path, fn + " - desc.txt")
save_file(path_, desc)
print(desc)
# print(prompt)


#thanks
system_txt = "You are a Horror story writer."
user_txt = "The audience on youtube has just listened to the horror story descibed here: " + str(chapter3) + ". /nCreate a thank you for listening greeting and remind audience to like and subscribe"
r = chatgpt3(system_txt + user_txt)
thanks = r.choices[0].message.content
path_ = os.path.join(xp_path, fn + " - thanks.txt")
save_file(path_, thanks)
print(thanks)




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
    #print(nc)
    
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
path_voice = os.path.join(xp_path, fn + " - thanks - audio_" + str(nc))
text2mp3(text_string = thanks, voice_name = "onyx", fn=path_voice )