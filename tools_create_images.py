#pip install Pillow
# pip install pydub
import re
import os
import openai
from openai import OpenAI
from time import time,sleep
import datetime



def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
        
openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)


# models
gpt4 = "gpt-4-1106-preview"
gpt3 = "gpt-3.5-turbo-1106"


# chatbot_role = open_file("chatbot_role.txt")
# chatbot_artist_role = open_file("chatbot_artist_role.txt")
# break_line = "\n" + 50*"-" + "\n"


# #chatbot
# def chatgpt3 (userinput, temperature=0.8, frequency_penalty=0.2, presence_penalty=0, system_role=chatbot_role, model = gpt4):
#     messagein = [
#         {"role": "user", "content": userinput },
#         {"role": "system", "content": system_role}]
#     response = client.chat.completions.create(
#         model = model,
#         temperature=temperature,
#         frequency_penalty=frequency_penalty,
#         presence_penalty=presence_penalty,
#         messages=messagein
#     )
#     text = response.choices[0].message.content
#     return response
# #####################################

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





def images_for_story(json_, story_no, image_count):
    images_pr_chapter = int(image_count)
    image_path = []
    nc = (story_no)*10
        
    for j in range(1, 1 + images_pr_chapter):
        print(j)
        system_txt = chatbot_artist_role

        user_txt = '''Select "image_prompt" from the json structure where "image_no." = ''' + str(j) + ''': \n
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


# image_files = []
# create_first_image()
# image_files = images_for_story(json_=r1_json, story_no=story_no)

