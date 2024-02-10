
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



#############################
## Create folder for export
#############################
# Create folder
cwd_path = os.getcwd()
xp_path_0 = "C:\\my\\__youtube\\videos"
additional_text = "horror"  # Replace with your desired text
xp_path = create_dated_folder(xp_path_0, additional_text)
# print(xp_path)


###################
# Define chatbot
###################
fn = "Stories"  #file name

break_line = "\n" + 50*"-" + "\n"

openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)

# models
gpt4 = "gpt-4-turbo-preview"
gpt3 = "gpt-3.5-turbo-1106"

# chatbot_role = open_file("chatbot_role.txt")
# chatbot_artist_role = open_file("chatbot_artist_role.txt")
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

# #3. add a message to the thread
# message = client.beta.threads.messages.create(
#     thread_id=thread.id, role="user",
#     # content="Can you write me 3 good titles for an Airbnb horror story?"
#     content = task
# )
# print(message)

# #4. run Assistant
# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
#     instructions="Please address user as Sir."
# )

# #5. Check the run status
# while True:
#     run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
#     print(f"Run status:{run.status}")
#     if run.status=='completed':
#         break
#     sleep(3)



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

t1 = '''I want you to write a short horror story to my youtube channel.
Insert these parameters in the description below

NUMBER = 3
GENRE = 'a horror story to a collection called "True Craigslist Horror Stories"'

Pitch Requirements:
	- Rooted in Realism: Each story must be grounded in reality, avoiding supernatural elements to ensure plausibility.
	- Narrative Style: Stories should be told in the first person, crafted as if recalled from memory, to enhance the authenticity and immersive experience.
	- Unique Twist: Incorporate an original twist that sets the story apart from conventional horror tales.
	- Intriguing Characters: Create characters that are complex and engaging, driving the narrative forward.
	- Emotional Stakes: Develop high emotional stakes that deeply invest the reader in the story's outcome.

Task List
	1. Write [NUMBER] of high-concept pitches for a bestselling [GENRE] story with a unique twist, intriguing characters, 
       and gripping emotional stakes and a breath taking ending.
	2. You are now a critique and a die hard fan of short horror stories. Use your experience to rate the pitches on a scale from 1-100. Stories that are not realistic should be rated very low 
	3. Select the the highest rated pitch. 
    4. REMEMBER TO WRITE IN 1ST PERSON. Write as if someone is telling the story from memory.
'''
r = new_msg(t1)
print(r)

t2 = '''
	4. For the selected pitch give me a highly detailed synopsis for a [GENRE] story in the traditional three act structure. Each act should be clearly labeled and should build toward the chosen ending.
	   Premise:
	   Ending:
    	Other Information:
	5. Write a character profile of the protagonist
    6. Using the created synopsis, create a detailed summary of the story, fleshing out additional details, and breaking it into parts
	7. Generate a list of 9 highly detailed action beats for a script with additional STORY INFORMATION to fully flesh out the chapter. 
       Make sure to always use proper nouns instead of pronouns.
	8. For each action beat create 1 image prompt that depicts the action
    - Make sure to describe persons on the images, so they are the right gender, age, race to support the story
    '''

r2 = new_msg(t2)
print(r2)

s1 = new_msg("Now write the story covering the intro and actionbeat 1-3.") 
# print(s1)
s2 = new_msg("Now write the story covering the intro and actionbeat 4-6.") 
# print(s2)
s3 = new_msg("Now write the story covering the intro and actionbeat 7-9 and the ending.") 
# print(s3)
image_prompts = new_msg("9. output nothing but the 9 image prompts in as a list.")
#print(l)
images_count = int(new_msg("How many image prompts are there? Output only the number."))
#print(images)
gender = new_msg("What gender is the protagonist? Output only [male/female/na].")

story = s1 + s2 + s3
count_words(story)

# print(story)
story_no = 1
path_story = os.path.join(xp_path, fn + " - story " + str(story_no) + ".txt")
save_file(path_story, story)
# print(path_story)

call text2mp3(story)  -  horror_tools
call prompt2img