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

fn = "AirBNB stories"
chapter_count = 3 # number of stories

chatbot_role = open_file("chatbot_role.txt")
chatbot_artist_role = open_file("chatbot_artist_role.txt")

task = open_file("task_AIRBNB.txt")
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



#######################
#### Shape user input
#######################
inspiration = open_file("Airbnb summaries.txt")
inspiration_task = '''
    1) Read the summaries below and create 5 summaries in same style but with different plots.
    Summaries for inspiration:
    ''' + inspiration + '''
    \n\nRead the summaries above and create 5 summaries in same style but with different plots and store them as a json struture. 
    Write in 1st person.
    NO  SUPERNATURAL STUFF, JUST BELIEVABLE EVENTS. 
   '''

def story_inspiration(user_input):  #suggest 5 plots from user input and rate them
    print(break_line + "story_inspiration")
    role = chatbot_role + task
    # prompt = role + "Suggest 5 detaked plots for a horrorstory from  these user inputs and store them as a json struture: " + user_input
    prompt = role + inspiration_task
    print(break_line + "prompt: \n" + prompt)
    r = chatgpt3(prompt, model = gpt4)
    stories_suggested = r.choices[0].message.content
    print(break_line + "stories_suggested:\n" + stories_suggested)
  
    #present 5 plot ideas and rate them
    role = chatbot_role + task
    prompt = role + '''Read the 5 plot suggestions one by one. Rate them from 1-100 and explain your rating. 
    Iif the story sounds supernatural or does not seem realistic then give a low rating.
    Add the rating and the explanation to the json structure and order it by descending rating. 
    Add a rank to each record.
    Only output the finished json structure\n''' + stories_suggested
    r = chatgpt3(prompt, model = gpt4)
    plots_rated = r.choices[0].message.content
    # plots_rated = break_line + prompt + break_line + rate_stories
    print(break_line + "plots_rated:\n" + plots_rated)
    return plots_rated

plots_rated = story_inspiration(user_input=inspiration_task) #  create 5 ideas based on user input


###############
# Select plot
def select_plot(plots_rated, rank = 1):
    role = chatbot_role + task
    prompt = role + "Output the json for the plot with rank = " + str(rank) + ":\n" + plots_rated
    r = chatgpt3(prompt, model = gpt4)
    selected_plot = r.choices[0].message.content
    print(break_line + "Selected plot:\n" + selected_plot)
    return selected_plot


##########¤¤¤¤¤¤¤#######
# Develop story idea
def develop_story_idea(selected_plot):
    role = chatbot_role + task
    prompt = role + "\nEvaluate the selected plot. \nSelected plot: " + selected_plot + break_line + '''
                    Based on inspiratpon above develop a story template for the story.
                    Create 6 action beats, a plot point, and a climax.
                    I want the story to be very scary.
                    REMEMBER IT NEEDS TO SOUND AUTHENTIC!
                    '''
    # print(prompt)

    r = chatgpt3(prompt, model = gpt4)
    story_idea = r.choices[0].message.content
    print(break_line + "\n" + story_idea + break_line)
    return story_idea
# story_idea = develop_story_idea(selected_plot)


#######################
## Write the story
def write_story(idea):
    role = chatbot_role + task
    task1 = "Read the draft below and write the story. follow the action beats. Write in great detail and in a vivid and intriguing language. Make sure to write in 1st person."
    task2 = "Read the draft above and write the story. follow the action beats. Write in great detail and in a vivid and intriguing language. Make sure to write in 1st person."
    task_write_chapter = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
    print("\n\nChapters")
    print(break_line)


    r = chatgpt3(task_write_chapter, model = gpt4)
    story_  = r.choices[0].message.content
    print(break_line + story_)
    count_words(story_)
    return story_
# story = write_story(idea = story_idea)



##########################################################
### LOOP over stories
##########################################################
chapters_ = []
plots_ = []
story_ideas_ = []
for chapter in range(1, chapter_count + 1):
    if chapter > 0:
        # print(chapter)
        selected_plot = select_plot(plots_rated, rank = chapter) #select best idea
        story_idea = develop_story_idea(selected_plot)
        story = write_story(idea = story_idea)
        
        plots_.append(selected_plot)
        story_ideas_.append(story_idea)
        chapters_.append(story)


# join stories
full_story = "\n".join(chapters_)
path_story = os.path.join(xp_path, fn + " - story.txt")
save_file(path_story, full_story)




################
## description
idea = plots_
role = chatbot_role + task
task1 = "Create a seo and youtube search optimized description to the youtube horror stories descibed in the json below. Use mark down and emojies.\n" 
task2 = "Create a seo and youtube search optimized description to the youtube horror story descibed in the json above. Use mark down and emojies." 
prompt = open_file("task_prompt.txt").replace("<<ROLE>>", role).replace("<<TASK1>>", task1).replace("<<IDEA>>", idea).replace("<<TASK2>>", task2)
# r = chatgpt3(prompt)
r = chatgpt3(prompt, model = gpt4)
desc = r.choices[0].message.content
path_ = os.path.join(xp_path, fn + " - desc.txt")
path_desc = path_
save_file(path_, desc)
print("\n\nDescription")
print(break_line)
print(prompt)
print(desc)
print(break_line)


###########
## thanks
system_txt = "You are a Horror story writer."
user_txt = "The audience has just listened to the Airbnb horror stories descibed  in the json below: " + str(plots_) + ". /nCreate a thank you for listening greeting and remind audience to like and subscribe"
r = chatgpt3(system_txt + user_txt, model = gpt4)
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
from datetime import datetime


#Dalle3
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



# 
def images_for_story(json_, chpt):
    images_pr_chapter = 6
    image_path = []
    image_files = []
    nc = (chpt + 1)*10
        
    for j in range(1, 1 + images_pr_chapter):
        print(j)
        system_txt = chatbot_artist_role
        user_txt = '''Can you help me create a perfect prompt for DALLE 3 for a horrifying image for this  airbnb horror story. 
        Make sure the image is dark and haunting, but unresistable. 
        DO NOT PUT TEXT ON THE IMAGE!!!. 
        End the prompt with the keywords: 4k, cinematic,vibrant, photorealistic, very scary. 
        Please write the prompt so it does not violate any copyright rights or content issues.
        --------------
        Base your prompt on "prompt" for this json structure where "img_no" = 1 : \n''' + js_

        r = chatgpt3 (userinput = user_txt, system_role=system_txt)
        img_prompt = r.choices[0].message.content
        print(img_prompt)

        rephrase_txt = '''If you get an error from Dalle related to content policy or something else when creating an image
        then rephrase the prompt and try again!
        '''
        dalle_prompt = img_prompt + break_line + rephrase_txt
        print(break_line + dalle_prompt)
        try:
            path_img = os.path.join(xp_path, fn + " - img")
        except:
            path_img = image_path[j - 1]
        image_path.append(path_img)
        
        image_url, filename = chatgpt_dalle(prompt = img_prompt, fn= path_img, i=nc + j)
        image_files.append(filename)
    return image_files

#create images and store location in image_lists: image_lists[0-n] contains images for story 0-n
image_lists =[]
for c in range(0, chapter_count):
    print(c)
    if c>=0:
        img_txt = story_ideas_[c]
        system_txt = "You are a data analyst."
        user_txt = "Select only the action beats from the json stucture. For each action beat create the perfect image prompt that captures the moment and output the image prompts in a new json structure with columns ['img_no', 'prompt']: " + img_txt
        r = chatgpt3(system_txt + user_txt, model = gpt4)
        js_ = r.choices[0].message.content
        print(js_)
        image_files = images_for_story(js_, c)
        image_lists.append(image_files)


##################
#   VOICE OVER   #
##################

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
import os


def text2mp3(text_string="testing", voice_name="onyx", fn="output"):
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



from moviepy.editor import AudioFileClip, concatenate_audioclips
# create voice for chapters
voice_files = []
for n,c in enumerate(chapters_):
    nc = n + 1
    print(nc)
    path_voice = os.path.join(xp_path, fn + " - audio_" + str(nc))
    print(path_voice)
    voice_files.append(path_voice)
    if nc>=0:
        text2mp3(text_string = c, voice_name = "echo", fn=path_voice)


#voice - thanks
path_voice = os.path.join(xp_path, fn + " - thanks - audio_99")
text2mp3(text_string = thanks, voice_name = "onyx", fn=path_voice )

gpt_story = '''I've always loved the thrill of exploring new places, so when David suggested a weekend getaway to a secluded Airbnb, I was instantly on board. The house, nestled in a dense forest, was the perfect blend of rustic charm and modern comfort, or so we thought.

From the moment we arrived, there was an air of mystery that I couldn't shake off. It started with small, odd occurrences – a missing loaf of bread, my favorite scarf misplaced, strange creaks in the night. David laughed it off, attributing it to my overactive imagination, but I couldn't help feeling unsettled.

One afternoon, while David was out grabbing some groceries, my curiosity led me to a small, barely noticeable door under the staircase. It was locked, but a hairpin and some persistence got me through. What I found was a narrow, creaking staircase spiraling down into darkness. With only the light from my phone guiding me, I descended.

The basement was cold, damp, and cluttered with old furniture and boxes. But what caught my eye was a makeshift living area in the corner, complete with a bed, some clothes, and personal belongings. It looked lived-in, and a chill ran down my spine. I quickly snapped a few photos with my phone and hurried back upstairs, locking the door behind me.

When David returned, I showed him the photos, and his skepticism turned to concern. We decided to confront the owner, but our calls went unanswered. That night, we heard footsteps above us. Grabbing a flashlight, David led the way as we cautiously searched the house.

In the living room, we came face-to-face with him – a disheveled, wild-eyed man. He introduced himself as Michael and claimed the house was his sanctuary. He spoke of how he'd been an Airbnb guest years ago and had never left, convinced the house belonged to him.

We tried to leave, but our car keys and phones were missing. Michael had hidden them, trapping us in his twisted reality. The next hours were a blur of panic and desperation as we tried to outsmart him. We managed to lock him in the basement, but in our haste, we stumbled upon a diary hidden in a floorboard.

The diary belonged to Michael. It chronicled his descent into madness and his obsession with the house. There were entries about us - how he'd watched us, moving our things, living amongst us unseen.

We finally found our keys and fled, driving away from that cursed place as fast as we could. But the terror of that night lingers. Michael's diary revealed a sinister connection to the house that we never fully understood, and I often wonder what other secrets lay hidden within its walls.

As we drove away, the sun was rising, casting light on the house that now seemed more like a prison than a sanctuary. I couldn't help but feel that we were leaving a part of ourselves behind, trapped in the pages of a madman's diary.

'''
gpt_story_2 ='''In the golden haze of a crisp autumn morning, I found myself driving down winding country roads, flanked by forests painted in fiery reds and glowing oranges. The air smelled of woodsmoke and the earthy scent of fallen leaves. It was the kind of setting where you'd expect nothing but peace and relaxation, a perfect escape from the city's perpetual clamor. I remember thinking how the quaint little town sprung up around the bend looked like something out of a storybook, untouched by time and the outside world's troubles. I was headed to an Airbnb I found online, touted for its seclusion and charm—a rustic cabin nestled at the edge of this picturesque town. It was supposed to be my haven for the next week, a place to recharge and maybe find inspiration hidden in the tranquility of nature. Little did I know that this so-called haven would soon become the setting of a memory I'd struggle to forget.

Action Beat 1: Getting to Know the Place Upon arrival, the cabin looked even more delightful than the pictures. Its wooden exterior was aged to a perfect patina, and it sat comfortably among the towering trees, as if it too had grown from the earth. The host, a man with a wiry frame and an easy smile named Martin, welcomed me with a warmth that felt a tad overzealous. He eagerly showed me around the small, cozy interior, adorned with antiques and warm, flickering lights. As he detailed the quirks of the cabin, I couldn't help but feel charmed by the place and its seemingly kind host.

Action Beat 2: Strange Noises and Distant Shadows The first night enveloped the cabin in utter darkness, the kind you only find far from the touch of city lights. It was then, in the depth of this darkness, that sleep escaped me, replaced by the unsettling sound of scratching coming from the basement's locked door. My heart raced as I lay in bed, listening intently, wondering if I was imagining things. The next evening, as the sun dipped below the trees casting long shadows, I spotted what looked like figures moving at the forest's edge. My pulse quickened, and a shiver ran down my spine—were there people watching the cabin?

Action Beat 3: The Host's Odd Behavior With unease settling in, I mentioned the noises and the shadows to Martin the following morning. His reaction was a chuckle, dismissing my concerns as city folk being unaccustomed to country life. But afterwards, his demeanor changed; his presence felt constant and suffocating, watching my every move with an unsettling intensity. My discomfort grew as my once-charming host's behavior twisted into something more invasive and unnerving.

Action Beat 4: Discovering Hidden Cameras Driven by a nagging suspicion and a growing sense of being watched, I started looking around—and that's when I found it. A tiny, almost invisible camera tucked away among the books on a shelf. Horror washed over me as the realization set in: Martin had been watching me. I confronted him, anger and fear tainting my voice, but he met my accusations with cold denial and an unsettling calm that did nothing to quell my terror.

Action Beat 5: A Tense Escape Plan I knew I had to leave, my mind racing to formulate an escape. Pretending to plan a lengthy hike, I packed my belongings with shaking hands, all while keeping a wary eye on Martin. He suggested driving me to a scenic spot, but the thought of being alone with him anywhere beyond the cabin's safety was unthinkable. The air was thick with tension; every second near him felt like a countdown to something much worse than being watched.

Action Beat 6: Narrow Escape Seizing a brief moment when Martin was distracted by a phone call, I slipped away, my heart pounding as I half-ran, half-stumbled through the woods, fearing at any moment I'd hear him behind me. But I didn't stop, not until I reached the safety of the town, where I immediately informed the authorities. Though Martin denied everything, leaving the incident shrouded in uncertainty, I was just grateful to be away from that cabin and its twisted host.

As I sit here recounting this memory, the feelings of fear and violation still grip me. The scenic beauty and tranquility that first drew me to that place now seem overshadowed by the shadows that lurked within. My escape was a stroke of luck, a fleeting chance grasped in a moment of sheer desperation. But what haunts me most is the nagging question: what might have happened if I hadn't left when I did?
'''
count_words(gpt_story_2)

path_voice = os.path.join(xp_path, fn + " - gpt_story_2")
text2mp3(text_string = gpt_story_2, voice_name = "shimmer", fn=path_voice )  #onyx = male. shimmer = female

#### create mp4 story wise
# image_lists[0-n]  -   images for story 0-n
# chapters_  - story 0-n
# voice_files - stories ib voice
##############################################3
from create_mp4 import *

#story1
n = 0 # story no.
audio_files = voice_files[n] + ".mp3"
image_files = image_lists[n]
output_mp4 = os.path.join(xp_path, "clip_" + str(n) + ".mp4")
    
# print(audio_path, " x ", image_paths, " = ", output_mp4)

# create_video_with_images_and_audio(image_paths=image_paths, audio_path=audio_path, output_filename=output_mp4, fps=30)
create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_files, output_filename=output_mp4, fps=30)





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
        image_paths = [os.path.join(xp_path, image_files[-1]), os.path.join(xp_path, image_files[-1])]

    audio_path = os.path.join(xp_path, audio_files[n])
    print(audio_path, " x ", image_paths, " = ", output_mp4)

    create_video_with_images_and_audio(image_paths=image_paths, audio_path=audio_path, output_filename=output_mp4, fps=30)

 
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
from add_music_to_mp4 import * 


output_final_mp4_music = os.path.join(xp_path,fn + "final_mp4_music.mp4")
add_ambient_music_to_video(
    video_file_path=output_final_mp4,
    music_folder_path='C:\\my\\__youtube\\videos\\horror_music',
    output_file_path=output_final_mp4_music,
    music_volume=0.05  # Adjust volume as needed
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
