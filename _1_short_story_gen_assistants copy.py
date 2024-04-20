
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



# select model
gpt4 = "gpt-4-turbo-preview"
gpt3 = "gpt-3.5-turbo"
selected_gpt = gpt4


#ideas - Valentines Day Stories; Tinder Stories; Home ALone Stories
fn = "Stories"  #file name
count_action_beats = 9
no_of_pitches = 3 # to select the best story


genre = "True Scary Tinder Dating Stories"
# genre = "True Walmart Horror Stories"
# genre = "Childhood stories"
# genre = "True AirBNB Horror Stories"
# genre = "True Exorcism Horror Stories"
# genre = "True Valentines Day Horror Stories"
# genre = "True Ouija Board Horror Stories"
# genre = "True Craigslist Horror Stories"
# user_input = "Make the story about a buyer that comes to a scary place to pick up a bought item" 
# user_input = "Make the story super scary and a psycological rollercoaster."
# user_input = "A Tinder date on Valentines Day that turns out horribly wrong. Make it super scary and a psycological rollercoaster."
# user_input = "A story about occultism, a young woman, a shaman, demons and exorcism - all happening in New York City. Make it super scary and a psycological rollercoaster."
# user_input = '''While browsing an antique store, Anna is drawn to a music box that releases a hidden amulet. The amulet possesses her, triggering strange occurrences around her. Seeking help, Anna learns the amulet is a dangerous artifact, but it becomes permanently attached to her, unleashing a demonic entity that attacks her friend Mark.'''
# user_input = '''Eleanor stumbles upon a hidden violin case in her inherited mansion, captivated by its melody and unsettling aura. Despite an inscription warning of untold secrets, she repairs the instrument. As she plays, the spirit of the previous owner appears, demanding she finish his unfinished music. Eleanor hesitates, sensing danger, but her passion for music compels her to play. The final notes echo, leaving her unconscious and the spirit vanished. When she awakens, she possesses unmatched skill, but her music holds no soul, hinting at the spirit's lingering influence.'''
# user_input = '''The protagonist arrives late at night in bad weather and has a hard time finding the key'''
#user_input = '''The story chronicles the experiences of a 10-year-old boy, Jake, who moves to a new town and forms a peculiar companionship with a neighborhood kid, Liam. Liam's strange behavior, including an unnerving welcome to his untidy home, makes Jake feel uncomfortable, forcing him to distance himself from Liam. The discomfort escalates into fear when Liam climbs into Jake's room at night. This culminates in a terrifying incident where Liam shatters Jake's window to enter his room, prompting Jake's parents to confront Liam's family and address the situation. While the immediate threat is averted, Jake is left with lingering unease as he moves on from the horrific incidents, pondering on what kind of adult Liam could have become.'''
# user_input = '''After a failed Ouija board attempt with their sister, a lone narrator tries again, inspired by online horror stories.  Footsteps and a muffled female voice emanate from upstairs, growing clearer as the narrator approaches their brother's room. The disembodied voice of their deceased grandmother echoes repeatedly, leaving the narrator terrified and shaken. This deeply personal encounter instills a lasting, vivid memory of terror.'''
user_input = ""
############################



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
# xp_path = r"C:\my\__youtube\videos\2024-02-29_1337_True Walmart Horror Stories"

###################
# Define chatbot
###################
break_line = "\n" + 50*"-" + "\n"

openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)

# # models
# gpt4 = "gpt-4-turbo-preview"
# gpt3 = "gpt-3.5-turbo"

system_role = open_file("chatbot_horror_writer_role.txt")
# task = open_file("assistant_horror_task.txt")
sleep(5)






#1. create assistant
assistant = client.beta.assistants.create(
    # instructions="You are a helpful assistant and a master of creating short horror stories",
    instructions = system_role,
    tools=[{"type": "code_interpreter"}],
    model = selected_gpt)

print(assistant)
print(assistant.id)   # asst_gmluHapfEinMNLGcSgvsbenO
sleep(5)


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
    tt = 0
    while True:
        t0 = 5
        tt = tt + t0
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Run status:{run.status} - " + str(tt) + " seconds.")
        if run.status=='completed':
            break
        sleep(t0)

    #Display messages when run completes
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value  # gets newest reponse from thread
    # print(response)
    return response
# r = new_msg("What is the gender of the protagonist")
# print(r)

t1_occultism = f'''
**Template for Occultism Horror Story Creation**

**Task: Create a Short Horror Story for My YouTube Channel**

**Pitch Requirements:**

- **Rooted in Occult Realism:** The story should weave elements of the occult mystique into a narrative that feels plausible within its own universe, subtly blending supernatural with the everyday.
- **Narrative Style:** The story must be told in the first person, giving the impression of a personal encounter with the occult. This approach should make the narrative feel as though it's being recounted from a deeply personal and unsettling memory.
- **Unique Occult Twist:** Incorporate a distinctive twist related to the occult that sets this story apart from typical horror narratives. This twist should be original and enhance the eerie atmosphere.
- **Complex Characters Involved with the Occult:** Develop characters that are multifaceted and drawn into the world of occultism through their interactions with occultism. These characters should drive the story, making their experiences compelling and relatable.
- **High Emotional and Supernatural Stakes:** Craft a story with significant emotional depth, where the stakes are amplified by the supernatural elements at play. The outcome should deeply affect the reader, making the occult experience resonate on a personal level.


**Task List:**

1. **Generate High-Concept Pitches:** Write {no_of_pitches} high-concept pitches for a best-selling horror story that delves into  occult themes. Each pitch should feature a unique twist, engaging characters, high emotional stakes, and an unforgettable ending. These pitches should be particularly terrifying, rooted in a first-person narrative as if someone is reliving a haunting memory. Base the pitches on user input ("{user_input}") if provided.
2. **Critique and Rate Pitches:** Assume the role of both a critic and an avid fan of short horror stories. Evaluate the pitches on a scale from 1-100, prioritizing stories that masterfully blend psychological terror with a touch of realism. Pitches that lack a believable foundation in the occult should receive lower ratings, while those that excel in psychological depth and terror should score higher.
3. **Select the Best Pitch:** Choose the pitch with the highest rating based on its psychological terror, and how effectively it employs the occult and ouija board elements.
4. **Output the Winning Pitch:** Present the selected pitch, its rating, and a detailed explanation for its top score. Highlight how it stands out in terms of its realistic approach to the occult, its emotional depth, and its unique, chilling twist.
'''

t1_tinder = f'''
**Template for Creating Tinder Dating Horror Stories**

**Task: Craft a Short Horror Story for My YouTube Channel**

**Pitch Requirements:**

**Rooted in Digital Dating Realism:** The story should delve into the eerie and unsettling experiences within the world of Tinder dating, portraying scenarios that are plausible and resonant with the realities of digital dating, yet tinged with horror.

**Narrative Style:** The narrative should be presented in the first person, offering an intimate recounting of a Tinder dating experience gone horribly wrong. This style should immerse the audience, making them feel as if they're listening to a friend share a deeply personal and terrifying story.

**Unique Dating Twist:** Incorporate a unique twist that transforms an ordinary Tinder date into an unforgettable horror story. This twist should be innovative and heighten the sense of dread, setting your story apart from typical dating horror tales.

**Complex Characters on Tinder:** Craft characters that are rich in depth and intricacy, with their motivations, backgrounds, and actions driving the narrative forward. Their interactions through Tinder should be central to the story, adding layers of complexity and suspense.

**High Emotional Stakes:** Build the story with significant emotional investment, where the stakes are personal and potentially devastating. The emotional journey should be compelling, intensifying the horror of the dating experience and making the story resonate on a deeper level.

Task List:

1. Generate High-Concept Pitches: Write {no_of_pitches} high-concept pitches for a captivating horror story set against the backdrop of Tinder dating. Each pitch should boast a unique twist, engaging characters, high emotional stakes, and a memorable ending that leaves the audience chilled. The narratives should be particularly harrowing, told in the first person to emphasize the personal horror of the dating experience. Include {user_input} for personalized pitches, if provided.

2. Critique and Rate Pitches: Take on the dual roles of critic and enthusiastic fan of short horror stories. Assess the pitches on a scale from 1-100, giving preference to those that skillfully combine psychological terror with the authenticity of digital dating experiences. Rate pitches that fail to capture the essence of Tinder dating lower, while those that excel in creating a palpable sense of fear and realism should score higher.

3. Select the Best Pitch: Identify the pitch that excels in depicting a Tinder dating scenario with genuine horror elements, scoring it based on its realism, psychological impact, and the creativity of its dating horror twist.

4. Output the Winning Pitch: Showcase the chosen pitch, its score, and the rationale behind its selection. Emphasize its strength in portraying a Tinder dating horror story that is both believable and deeply unsettling, with a unique twist and emotional depth that truly engages and horrifies the audience.

'''

t1_ouija = f'''
**Template for Ouija Board and Occultism Horror Story Creation**

**Task: Create a Short Horror Story for My YouTube Channel**

**Pitch Requirements:**

- **Rooted in Occult Realism:** The story should weave elements of the occult and ouija board mystique into a narrative that feels plausible within its own universe, subtly blending supernatural with the everyday.
- **Narrative Style:** The story must be told in the first person, giving the impression of a personal encounter with the occult. This approach should make the narrative feel as though it's being recounted from a deeply personal and unsettling memory.
- **Unique Occult Twist:** Incorporate a distinctive twist related to the occult or ouija board that sets this story apart from typical horror narratives. This twist should be original and enhance the eerie atmosphere.
- **Complex Characters Involved with the Occult:** Develop characters that are multifaceted and drawn into the world of occultism through their interactions with a ouija board. These characters should drive the story, making their experiences compelling and relatable.
- **High Emotional and Supernatural Stakes:** Craft a story with significant emotional depth, where the stakes are amplified by the supernatural elements at play. The outcome should deeply affect the reader, making the occult experience resonate on a personal level.


**Task List:**

1. **Generate High-Concept Pitches:** Write {no_of_pitches} high-concept pitches for a best-selling horror story that delves into ouija boards and occult themes. Each pitch should feature a unique twist, engaging characters, high emotional stakes, and an unforgettable ending. These pitches should be particularly terrifying, rooted in a first-person narrative as if someone is reliving a haunting memory. Base the pitches on user input ("{user_input}") if provided.
2. **Critique and Rate Pitches:** Assume the role of both a critic and an avid fan of short horror stories. Evaluate the pitches on a scale from 1-100, prioritizing stories that masterfully blend psychological terror with a touch of realism. Pitches that lack a believable foundation in the occult should receive lower ratings, while those that excel in psychological depth and terror should score higher.
3. **Select the Best Pitch:** Choose the pitch with the highest rating based on its psychological terror, and how effectively it employs the occult and ouija board elements.
4. **Output the Winning Pitch:** Present the selected pitch, its rating, and a detailed explanation for its top score. Highlight how it stands out in terms of its realistic approach to the occult, its emotional depth, and its unique, chilling twist.
'''
t1_airbnb = '''Task Description:
I want you to help me create a pitch for a psychological horror story for my YouTube channel.


Key points:
- Rooted in Realism: The story should be grounded in reality, avoiding supernatural elements and focusing instead on the unsettling potential of ordinary events and human behavior.
- Narrative Style: First person, told as if recalling a personal experience. The storytelling should effectively convey the growing sense of unease and fear.
- Compelling Hook: Start with a powerful opening that draws the audience into the unsettling atmosphere of the Airbnb and introduces the strange occurrences.
- Unique Twist: Instead of a supernatural revelation, the story should have an open ending that leaves viewers questioning reality and their own perceptions.
- Intriguing Characters: Create compelling characters, particularly the host and their own complexities.
- Emotional Stakes: Highlight the protagonist's emotional journey as they navigate the unsettling situation and question their own sanity.


Task:
- Write 1 high-concept pitch for a YouTube horror story centered around an unsettling Airbnb experience. Base them on user input ("{user_input}") if any.  
- Incorporate the following elements:
  - A protagonist (not named) looking for a relaxing getaway in a remote location
  - An unusual Airbnb host with unsettling behavior.
  - A series of seemingly mundane but increasingly disturbing events that take place in the Airbnb.
  - An open ending that leaves the audience questioning the nature of reality and the host's motives.

  
Remember:
* Write in the first person (as if recalling the experience).
* Avoid supernatural elements.


Additional Notes:
Feel free to add details to enhance the atmosphere and build tension.
Focus on crafting the pitch within the YouTube format, keeping the audience engaged throughout.
By omitting supernatural elements and focusing on the psychological impact of mundane events and bizarre behavior, this refined task description aims to create a more unsettling and thought-provoking horror story.'''


t1_walmart = '''
Task Description:
I want you to help me create a pitch for a psychological horror story for my YouTube channel.


Key points:
- Rooted in Realism: The story should be grounded in reality, avoiding supernatural elements and focusing instead on the unsettling potential of ordinary events and human behavior within the confines of a Walmart.
- Narrative Style: First person, told as if recalling a personal experience. The storytelling should effectively convey the growing sense of unease and fear.
- Compelling Hook: Start with a powerful opening that draws the audience into the unsettling atmosphere of the Walmart and introduces the strange occurrences.
- Unique Twist: Instead of a supernatural revelation, the story should have an open ending that leaves viewers questioning reality and their own perceptions.
- Intriguing Characters: Create compelling characters, particularly Walmart employees or other shoppers with their own complexities.
- Emotional Stakes: Highlight the protagonist's emotional journey as they navigate the unsettling situation within Walmart and question their own sanity.


Task:
Write 1 high-concept pitch for a YouTube horror story centered around an unsettling Walmart experience. Base them on user input ("{user_input}") if any.  


Incorporate the following elements:
- A protagonist (not named) looking for a quick, mundane shopping trip turned nightmarish.
- An unusual Walmart employee or fellow shopper with unsettling behavior.
- A series of seemingly mundane but increasingly disturbing events that take place within the Walmart.
- An open ending that leaves the audience questioning the nature of reality and the motives of the people they encountered.


Remember:
* Write in the first person (as if recalling the experience).
* Avoid supernatural elements.


Additional Notes:
Feel free to add details to enhance the atmosphere and build tension.
Focus on crafting the pitch within the YouTube format, keeping the audience engaged throughout.
By omitting supernatural elements and focusing on the psychological impact of mundane events and bizarre behavior, this refined task description aims to create a more unsettling and thought-provoking horror story.'''



t1_event_focused = f'''
I want you to write a short {genre} story for my YouTube channel.
Pitch Requirements:
	- Rooted in Realism: The story must be grounded in reality, avoiding elements that conflict with the genre's plausibility, yet allowing for one extraordinary event or act that intensifies the narrative.
	- Narrative Style: Stories should be told in the first person, crafted as if recalled from memory. The storytelling should effectively convey the intensity and scariness of the extraordinary event, making it feel real and immediate.
	- Compelling Hook: Start with a powerful opening that sets up the extraordinary event or act. The hook should be intriguing, drawing the audience in to uncover the mystery or deal with the aftermath.
	- Unique Twist: Incorporate an original twist related to the extraordinary event that sets the story apart from conventional {genre} tales.
	- Intriguing Characters: Create characters that are complex and engaging, with their fates intertwined with the extraordinary event. Their reactions and decisions should drive the narrative forward.
	- Emotional Stakes: Develop high emotional stakes centered around the extraordinary event, deeply investing the reader in the story's outcome.

Task List:
	1. Write {no_of_pitches} high-concept pitches for a bestselling {genre} story, each centered around an extraordinary event or act that, given the circumstances and the way it is told, makes the story intense and scary. Include a compelling hook, a unique twist, intriguing characters, and gripping emotional stakes with a breathtaking ending. Base them on user input ("{user_input}") if any. The pitches must align with the {genre} theme.
       Try not to use the most common names like Alex, Jamie, etc.
       REMEMBER TO WRITE IN 1ST PERSON. Write as if someone is telling the story from memory.
	2. You are now a critique and a die-hard fan of {genre} stories. Use your experience to rate the pitches on a scale from 1-100, especially considering the effectiveness of the extraordinary event in making the story intense and scary, realism within the {genre} context, and other elements valued in {genre}.
	3. Select the highest rated pitch based on its effectiveness in leveraging the extraordinary event to create intensity and fear, realism, and genre alignment.
    4. Output the selected pitch, its rating, and the reason for why it got the best rating, with a focus on how the extraordinary event enhances the story's intensity and scariness.
'''
#realism
t1_realism = f'''
I want you to write a short horror story to my youtube channel.
Pitch Requirements:
	- Rooted in Realism: The story must be grounded in reality, avoiding supernatural elements to ensure plausibility.
	- Narrative Style: Stories should be told in the first person, crafted as if recalled from memory, to enhance the authenticity and immersive experience.
	- Unique Twist: Incorporate an original twist that sets the story apart from conventional horror tales.
	- Intriguing Characters: Create characters that are complex and engaging, driving the narrative forward.
	- Emotional Stakes: Develop high emotional stakes that deeply invest the reader in the story's outcome.

Task List
	1. Write {no_of_pitches} of high-concept pitches for a bestselling {genre} story with a unique twist, intriguing characters, 
       and gripping emotional stakes and a breath taking ending. Base them on user input ("{user_input}") if any.
       The pitches must be very scary.
       Try not to use the most common names like Alex, Jamie etc.
       REMEMBER TO WRITE IN 1ST PERSON. Write as if someone is telling the story from memory.
	2. You are now a critique and a die hard fan of short horror stories. Use your experience to rate the pitches on a scale from 1-100. Stories that are not realistic should be rated very low. Psychological terror should rate high.
	3. Select the the highest rated pitch. 
    4. Output the selected pitch, its rating and the reason for why it got the best rating.
'''

t1_childhood_stories = ''' Task Description: I want you to help me create a pitch for a real-life horror story based on disturbing childhood memories for my YouTube Channel.

Key points:

Rooted in Realism: The story should be grounded in reality, focusing on unsettling events and strange behaviors that occur during childhood. Avoid supernatural elements.
Narrative Style: First person, told as if recalling an actual childhood experience. The storytelling should effectively convey the growing unease and fear.
Compelling Hook: Start with a powerful opening that introduces the unsettling atmosphere of the new neighborhood or school and the strange occurrences.
Unique Twist: Instead of a supernatural revelation, the story should have an open ending that keeps viewers questioning reality and their own childhood experiences.
Intriguing Characters: Create compelling characters, particularly kids or adults in the neighborhood with their own complexities.
Emotional Stakes: Highlight the protagonist's emotional journey as they navigate the unsettling situation during their childhood and question their own sanity.
Task: Write 1 high-concept pitch for a YouTube horror story centered around a disturbing childhood experience. Base it on user input ("{user_input}") if any.

Incorporate the following elements:

A protagonist moving to a new neighborhood or school turned into a nightmare.
A neighborhood or school kid or an adult with unsettling behavior.
A series of ordinary but increasingly disturbing events during childhood.
An open ending that leaves the audience questioning the nature of reality and the motives of the people they encountered.
Remember:

Write in the first person (as if recalling the experience).
Avoid supernatural elements.
Additional Notes: Feel free to add details to enhance the atmosphere and build tension. Focus on crafting the pitch within the YouTube format, maintaining audience engagement throughout. By omitting supernatural elements and focusing on the psychological impact of mundane events and bizarre behavior, this refined task description aims to create a more unsettling and thought-provoking real-life horror story. '''
t1 = t1_tinder
# t1 = t1_childhood_stories
# t1 = t1_ouija
# t1 = t1_airbnb
# t1 = t1_walmart
# t1 = t1_event_focused
# t1 = t1_realism
r = new_msg(t1)
print(r)


t2 = f'''
Tasks for writing the story
	5. For the selected pitch give me a highly detailed synopsis for a {genre} story in the traditional three act structure. Each act should be clearly labeled and should build toward the chosen ending.
	   Premise:
	   Ending:
    	Other Information:
    6. Character Profile Creation
    - Protagonist Profile: Begin by choosing a gender for the protagonist. Describe their physical appearance in detail, including height, body type, race, hair color and style, eye color, and any distinctive features such as scars or tattoos. Mention their typical attire or clothing style, fitting the story's context. Include personality traits, skills, and backstory relevant to their role in the story.
    - Supporting Characters Profiles (up to 2): Identify up to two key supporting characters and provide a detailed description for each, following the same structure as for the protagonist. Ensure these characters have distinct appearances, attire, and personalities to complement the protagonist and contribute to the story's dynamics.

    7. Detailed Story Summary
    - Using the created synopsis, craft a structured summary of the story, integrating the protagonist and up to two key supporting characters. Describe how these characters interact with each other and the plot.
    - Break down the narrative into intro and compelling hook, beginning, middle, and end, including setting descriptions, key events, character development arcs, main conflict, and resolution. Make sure to begin with a compelling hook that makes the audience want to stay.
    - Organize the story into distinct parts or chapters, detailing the roles and evolution of the protagonist and supporting characters throughout.

    8. Action Beats for Script
    - List {count_action_beats} detailed action beats crucial for the storys development, ensuring the protagonist remains the focal point while integrating up to two supporting characters in these scenes.
    - For each action beat, provide comprehensive STORY INFORMATION, including setting, character emotions and motivations, and the beat's outcome. Highlight interactions between the protagonist and supporting characters, showcasing their importance to the story and character development.
'''

r2 = new_msg(t2)
print(r2)

s1 = new_msg("Now write part 1 of the story covering the intro and actionbeat 1-3. Output nothing but part 1 of the story.") 
# print(s1)
s2 = new_msg("Now write part 2 of the story covering actionbeat 4-6. Output nothing but part 2 of the story.") 
# print(s2)
s3 = new_msg("Now write part 3 of the story covering actionbeat 7-9 and the ending. Output nothing but part 3 of the story.") 
# print(s3)

story = s1 + s2 + s3
count_words(story)

#save story
story_no = 1
path_story = os.path.join(xp_path, fn + " - story " + str(story_no) + ".txt")
save_file(path_story, story)

gender = new_msg("What gender is the protagonist? Output only [male/female].")
print(gender)

desc = new_msg("Create a good title and a small teaser for this story to be used in a youtube description. Outout only that.")
path_desc = os.path.join(xp_path, fn + " - desc_ " + str(story_no) + ".txt")
save_file(path_desc, desc)

# story = open_file(r"C:\my\__youtube\videos\2024-02-29_1337_True Walmart Horror Stories\Stories - story 1.txt")


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
                    - Ensure that style of the image is consistent across all the images. Make the images photo realistic, Hasselblad.
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

#create thumbnail
def create_thumbnail(user_input = ""):
    path_img = os.path.join(xp_path, fn + " - thumbnail_")
    query = '''Use your talents as digital artist to create a detailed image prompt for a thumbnail to this story on youtube,
            ''' + user_input + '''
            Make sure the prompt complies with OpenAIs policy for image generation. Do not mention any brands.'''
    img_prompt = new_msg(query) 
    image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn= path_img, i=100)
    # image_files_.append(filename)

create_thumbnail("")
# create_thumbnail("Portrait the house the story is happening in")

####################
# Create voice over
####################
import tools_voice_over as tvo
def create_voice_over(gender):
    path_voice = os.path.join(xp_path, fn + " - " + str(story_no))

    search_term = "female"
    if search_term.lower() in gender.lower():
        gender = "female"
    else:
        gender = "male"

    if gender=="female":
        voice = "shimmer"
    else:
        voice = "onyx"
    tvo.text2mp3(text_string = story, voice_name = voice, fn=path_voice )
    audio_file = path_voice + ".mp3"
    return audio_file

audio_file = create_voice_over(gender)
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
from tools_create_mp4_delete import *
def create_mp4(output_mp4):
    create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)
    count_words(story)

output_final_mp4 = os.path.join(xp_path, "clip_" + str(story_no) + ".mp4")
create_mp4(output_mp4 = output_final_mp4)


###########################
# Adding music sound track
###########################
# from add_music_to_mp4 import * 
# import add_music_to_mp4 as am
# output_final_mp4_music = os.path.join(xp_path,fn + "final_mp4_w_music.mp4")
# am.add_ambient_music_to_video(
#     video_file_path=output_final_mp4,
#     music_folder_path='C:\\my\\__youtube\\videos\\horror_music',
#     output_file_path=output_final_mp4_music,
#     music_volume=0.05  # Adjust volume as needed
#     )

