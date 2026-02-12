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
        
openai_api_key = open_file('/Users/lasse/Desktop/my/Git/api-keys/openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)


# models
# gpt4 = "gpt-4-1106-preview"
# gpt3 = "gpt-3.5-turbo-1106"
gpt4 = "gpt-4o"
# gpt4 = "gpt-4-turbo"
gpt3 = "gpt-3.5-turbo"
selected_gpt = gpt4


import tools_query_chatbot as tqc        
def improve_image_prompt(p1):
    gpt4 = "gpt-4.1"  # gpt4 model selection    p1 = "User_prompt: \n " + str(p0) + "\n----------\n "
    p2 = open_file("/Users/lasse/Desktop/my/Git/horror_story_trimmed/prompt_library/prompt_images_story.md")
    p3 = "OUTPUT NOTHING BUT THE IMAGE PROMPT!"
    px = p1 + p2 + p3
    img_prompt = tqc.chatgpt(userinput=px, system_role="You are a helpful assistant", model=gpt4)
    return img_prompt
#ip = improve_image_prompt("dark background image for scary story. No persons, just dark and scary")


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
        #model="dall-e-3",
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
    filename = f"{fn}_{datetime_string}.png"
    image.save(filename)
    print("save(filename): " + str(filename))
    # Return the image URL and the path to the saved image file
    return image_url, filename
#image_url, filename = chatgpt_dalle("a blue cat", fn="my_cat_image_", i=42)
#image_url, filename = chatgpt_dalle(prompt2, fn="my_cat_image_", i=42)
#img_dalle3 = chatgpt_dalle(prompt="A white siamese cat balancing on a sign saying TEST", fn="image", i=1)
#prompt1 = '''Super Scary Image Prompt: Cemetery
#Imagine a bone-chilling, ultra-realistic scene set in an ancient, overgrown cemetery at midnight. The moon is shrouded by thick, swirling clouds, casting only faint, silvery light that barely illuminates the crumbling tombstones and crooked, rusted iron gates. Dense, unnatural fog coils around the graves, obscuring the ground and making the shadows seem alive. Gnarled, leafless trees loom overhead, their twisted branches reaching out like skeletal fingers. In the foreground, a freshly dug grave gapes open, its edges jagged and raw, as if something has recently clawed its way out. Faint, ghostly figures drift between the headstones, their faces hollow and eyes glowing with an eerie, unnatural light. One spectral figure stands at the foot of the open grave, its tattered burial shroud fluttering in a wind that cannot be felt, its mouth stretched wide in a silent scream. Scattered throughout the scene, flickering candles and wilted flowers hint at forgotten rituals and lost souls. The entire image is saturated with deep shadows, cold blue and sickly green highlights, and a sense of overwhelming dread, as if the cemetery itself is watching and waiting for the living to stray too close.'''
#prompt2 = '''Super Scary Image Prompt: Lonely Cabin in the Woods
#QPicture an ultra-realistic, spine-chilling scene deep in a dense, ancient forest under a pitch-black, moonless sky. At the center stands a small, decrepit wooden cabin, its windows shattered and door hanging crookedly on rusted hinges. The cabin is barely illuminated by a single, flickering lantern on the porch, casting long, distorted shadows that seem to move on their own. The surrounding trees are impossibly tall and twisted, their bark gnarled and blackened, with thick, tangled roots snaking across the ground like grasping hands. A thick, unnatural mist creeps along the forest floor, swirling around the cabin and obscuring what might be lurking just out of sight. In the darkness beyond the lantern’s glow, faint, ghostly shapes can be glimpsed—pale faces with hollow eyes peering from between the trees, and elongated, shadowy figures standing motionless in the fog. The air is heavy with a sense of isolation and menace, as if the forest itself is alive and closing in, and the cabin is the last fragile refuge before something unspeakable emerges from the gloom.'''
#ip = improve_image_prompt("dark background image for scary story. No persons, no light, just dark and scary")
#image_url, filename = chatgpt_dalle(ip, fn="dark_bg_image_", i=42)
#ip = improve_image_prompt("Hyperrealistic masterpiece, 8K resolution, 16:9 aspect ratio, cinematic shot. A modern police cruiser has skidded to a halt on a narrow, snow-covered forest road at night. Its headlights are on full beam and emergency lights (vibrant red and blue) are actively flashing. Heavy snow is falling.  Color palette: inky blacks/blues, stark white snow, intense white headlight beams, vibrant red/blue emergency lights. Atmosphere of sudden shock, intense confrontation, immediate threat, and chilling mystery. Style reminiscent of a stark thriller confrontation. Highly detailed, sharp focus on the immediate scene with dynamic falling snow.")
#image_url, filename = chatgpt_dalle(ip, fn="police_car", i=42)


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


def create_images(images):
    image_error_path = "/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/cemetary1024p.png"
    for i in range(0, len(images)):
        img_prompt0 = str(images[0])
        print(i, "orig prompt:\n ",img_prompt0, "\n ---------------------")

        #improve image prompt
        img_prompt = tci.improve_image_prompt(img_prompt0)
        print(img_prompt, "\n ---------------------")

        path_img = filename_without_extension + "-img_" + str(i)

        try:  #if no image or if problem with image then reuse the former
            image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn=path_img)
            image_files.append(filename)
            # Renaming logic is now handled after this call
        except:
            try:
                img_prompt = new_msg(f"This prompt was declined by Dall-e. Please rephrase it  carefully: {img_prompt}")
            except:
                if i>1:
                    image_files.append(image_files[-1])
                else:
                    image_files.append(image_error_path)
                    error_list.append(f"Error_default_image in position {i} in function create_images()")
