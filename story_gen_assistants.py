
#pip install Pillow
# pip install pydub
import re
import os
import openai
from openai import OpenAI
from time import time,sleep
import datetime

####################
# Story settings
####################

#ideas - Valentines Day Stories; Tinder Stories; Home ALone Stories
fn = "Stories"  #file name
count_action_beats = 7

no_of_pitches = 3
genre = "True Craigslist Horror Stories"
# user_input = "Make the story about a buyer that comes to a scary place to pick up a bought item" 
user_input = ""


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



#############################
## Create folder for export
#############################
# Create folder
cwd_path = os.getcwd()
xp_path_0 = "C:\\my\\__youtube\\videos"
additional_text = genre  # Replace with your desired text
xp_path = create_dated_folder(xp_path_0, additional_text)
# print(xp_path)


###################
# Define chatbot
###################
break_line = "\n" + 50*"-" + "\n"

openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)

# models
gpt4 = "gpt-4-turbo-preview"
gpt3 = "gpt-3.5-turbo-1106"

system_role = open_file("chatbot_horror_writer_role.txt")
# task = open_file("assistant_horror_task.txt")

#1. create assistant
assistant = client.beta.assistants.create(
    # instructions="You are a helpful assistant and a master of creating short horror stories",
    instructions = system_role,
    tools=[{"type": "code_interpreter"}],
    model = gpt4)

print(assistant)
print(assistant.id)   # asst_gmluHapfEinMNLGcSgvsbenO

#2. create thread
thread = client.beta.threads.create()
print(thread)
print(thread.id) # thread_RUAndXpEbqXiXrtKx2MC0Fu5
thread_id = thread.id


def new_msg(task):
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user",
        # content="Can you write me 3 good titles for an Airbnb horror story?"
        content = task
    )
    
    #run Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address user as Sir."
    )

    #Check the run status
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Run status:{run.status}")
        if run.status=='completed':
            break
        sleep(5)

    #Display messages when run completes
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value  # gets newest reponse from thread
    # print(response)
    return response
# r = new_msg("What is the gender of the protagonist")
# print(r)



t1 = f'''
I want you to write a short horror story to my youtube channel.
Pitch Requirements:
	- Rooted in Realism: The story must be grounded in reality, avoiding supernatural elements to ensure plausibility.
	- Narrative Style: Stories should be told in the first person, crafted as if recalled from memory, to enhance the authenticity and immersive experience.
	- Unique Twist: Incorporate an original twist that sets the story apart from conventional horror tales.
	- Intriguing Characters: Create characters that are complex and engaging, driving the narrative forward.
	- Emotional Stakes: Develop high emotional stakes that deeply invest the reader in the story's outcome.

Task List
	1. Write {no_of_pitches} of high-concept pitches for a bestselling {genre} story with a unique twist, intriguing characters, 
       and gripping emotional stakes and a breath taking ending. Base them on {user_input} if any.
       The pitches must be very scary.
       REMEMBER TO WRITE IN 1ST PERSON. Write as if someone is telling the story from memory.
	2. You are now a critique and a die hard fan of short horror stories. Use your experience to rate the pitches on a scale from 1-100. Stories that are not realistic should be rated very low. Psychological terror should rate high.
	3. Select the the highest rated pitch. 
    4. Output the selected pitch, its rating and the reason for why it got the best rating.
'''
r = new_msg(t1)
print(r)


t2 = f'''
	5. For the selected pitch give me a highly detailed synopsis for a [GENRE] story in the traditional three act structure. Each act should be clearly labeled and should build toward the chosen ending.
	   Premise:
	   Ending:
    	Other Information:
    6. Character Profile Creation
    - Protagonist Profile: Begin by choosing a gender for the protagonist. Describe their physical appearance in detail, including height, body type, race, hair color and style, eye color, and any distinctive features such as scars or tattoos. Mention their typical attire or clothing style, fitting the story's context. Include personality traits, skills, and backstory relevant to their role in the story.
    - Supporting Characters Profiles (up to 2): Identify up to two key supporting characters and provide a detailed description for each, following the same structure as for the protagonist. Ensure these characters have distinct appearances, attire, and personalities to complement the protagonist and contribute to the story's dynamics.

    7. Detailed Story Summary
    - Using the created synopsis, craft a structured summary of the story, integrating the protagonist and up to two key supporting characters. Describe how these characters interact with each other and the plot.
    - Break down the narrative into beginning, middle, and end, including setting descriptions, key events, character development arcs, main conflict, and resolution.
    - Organize the story into distinct parts or chapters, detailing the roles and evolution of the protagonist and supporting characters throughout.

    8. Action Beats for Script
    - List {count_action_beats} detailed action beats crucial for the chapter's development, ensuring the protagonist remains the focal point while integrating up to two supporting characters in these scenes.
    - For each action beat, provide comprehensive STORY INFORMATION, including setting, character emotions and motivations, and the beat's outcome. Highlight interactions between the protagonist and supporting characters, showcasing their importance to the story and character development.
'''

r2 = new_msg(t2)
print(r2)

s1 = new_msg("Now write part 1 of the story covering the intro and actionbeat 1-3. Output nothing but part 1 of the story.") 
# print(s1)
s2 = new_msg("Now write part 2 of the story covering the intro and actionbeat 4-6. Output nothing but part 2 of the story.") 
# print(s2)
s3 = new_msg("Now write part 3 of the story covering the intro and actionbeat 7-9 and the ending. Output nothing but part 3 of the story.") 
# print(s3)

story = s1 + s2 + s3
count_words(story)

#save story
story_no = 1
path_story = os.path.join(xp_path, fn + " - story " + str(story_no) + ".txt")
save_file(path_story, story)


gender = new_msg("What gender is the protagonist? Output only [male/female].")
print(gender)


####################
# Create images
####################
import tools_create_images as tci

def create_images():
    image_desc = []
    for i in range(1, count_action_beats+1):
    # for i in range(1, 2+1):
        print(i)
        prompt = f'''
                Use your talents as digital artist to create a detailed image prompt for action beat {i}. 
                Focusing on visualizing the scene with the protagonist always as the primary focus.
                    - Describe the protagonist and up to two supporting characters involved in the scene, ensuring their appearances, expressions, and attire are detailed for consistency across images.
                    - Include setting details (time of day, location), important objects, and environmental elements to convey the mood or atmosphere.
                    - Ensure that style of the image is consistent across all the images.
                    - Ensure the protagonist's prominence in the scene, with supporting characters positioned to highlight their relationship and interactions with the protagonist.
                    - Make sure the prompt complies with OpenAIs policy for image generation. Do not mention any brands.
                '''

        img_prompt = new_msg(prompt)
        print(break_line + "image prompt: " + str(i) + "\n" + img_prompt)

        # rephrase_txt = '''If you get an error from Dall-e related to content policy or something else when creating an image
        # then rephrase the prompt and try again!'''
        
        # dalle_prompt = img_prompt + break_line
        # print(break_line + dalle_prompt)
        path_img = os.path.join(xp_path, fn + " - img")
        
        try:  #if no image or if problem with image then reuse the former
            image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn= path_img, i=10 + i)
            image_files.append(filename)
        except:
            image_files.append(image_files[-1])

        image_desc.append(str(img_prompt))
    
    path_img_desc = os.path.join(xp_path, fn + " - image_desc - story " + str(story_no) + ".txt")
    save_file(path_img_desc, str(image_desc))

image_files = []
create_images()
# image_files = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".png")]



####################
# Create voice over
####################
import tools_voice_over as tvo
def create_voice_over():
    path_voice = os.path.join(xp_path, fn + " - " + str(story_no))
    if gender=='female':
        voice = "shimmer"
    else:
        voice = "onyx"
    tvo.text2mp3(text_string = story, voice_name = voice, fn=path_voice )
    audio_file = path_voice + ".mp3"
    return audio_file

audio_file = create_voice_over()
# audio_files = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".mp3")]
# audio_file = audio_files[0]




##############################################
#### create mp4 - images and voice
# image_files[]  -   image list for story
# story  - text for current story
# audiofile - current story voice over
# story_no -  current story no.
#   
##############################################
from create_mp4 import *
def create_mp4():
    output_mp4 = os.path.join(xp_path, "clip_" + str(story_no) + ".mp4")
    create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)
    count_words(story)

create_mp4()
