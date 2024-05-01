import os
# from tools_create_mp4 import *
import tools_create_mp4 as tcm
from time import time  , sleep
import datetime
import _1_short_story_gen_assistants as story_gen
###########################
# ############# walmart stories
# title_compilation = "TRUE Scary Walmart Stories"
# num_stories = 7
# story_type = "Walmart" # controls the storygenerator functions
# genre = "Truly Scary Walmart Stories"
# user_input = ""
# optimized_search_phrases ="Scary Walmart Stories", "Walmart Horror Stories"
# general_seo_phrases = "true horror stories","true scary stories", "reddit stories"
# ##########################


# ##########################
# ##### Tinder/dating Stories
# title_compilation = "TRUE Scary Dating Stories"
# num_stories = 7
# story_type = "tinder" # controls the storygenerator functions
# genre = "Truly Scary tinder online dating Stories"
# user_input = ""
# optimized_search_phrases ="Scary Tinder Dating Stories", "Tinder Dating Horror Stories"
# general_seo_phrases = "true horror stories","true scary stories", "reddit stories"
# # ##########################


# ##########################
# ##### Highschool Stories
# title_compilation = "TRUE Scary Highschool Stories"
# num_stories = 3
# story_type = "Highschool" # controls the storygenerator functions
# genre = "Truly Scary Highschool Stories"
# user_input = ""
# optimized_search_phrases ="Scary High School Stories", "High School Horror Stories"
# general_seo_phrases = "true horror stories","true scary stories", "reddit stories"
# ##########################


# ##########################
# ##### Voodoo_dark_magic Stories
# title_compilation = "Scary Stories about vodoo and black magic"
# num_stories = 3
# story_type = "voodoo_dark_magic" # controls the storygenerator functions
# genre = "Scary Voodoo Stories"
# user_input = ""
# optimized_search_phrases ="Scary Black Magic Stories", "Voodoo Horror Stories"
# general_seo_phrases = "true horror stories","true scary stories", "reddit stories"
# ##########################


#############################
##South Korean Horror Stories
# title_compilation = "TRUE Scary  South Korean Horror Stories"
# num_stories = 4
# story_type = "South Korean" # controls the storygenerator functions
# genre = "Truly Scary South Korean Horror Stories"
# user_input = ""
# optimized_search_phrases ="Scary outh Korean Horror Stories", " South Korean Horror Stories"
# general_seo_phrases = "asian horror stories","true scary stories", "reddit stories"
############################


###########################
############# ouija stories
title_compilation = "TRUE Scary ouija board Stories From The Internet | True Scary Stories"
num_stories = 6
story_type = "Ouija" # controls the storygenerator functions
genre = "Truly Scary Ouija Stories"
user_input = ""
optimized_search_phrases ="Scary Ouija Board Stories", "Ouija Board Horror Stories"
general_seo_phrases = "true horror stories","true scary stories", "reddit stories"
# ##########################

###########################
# ############# walmart stories
# title_compilation = "TRUE Scary Walmart Stories"
# num_stories = 7
# story_type = "Walmart" # controls the storygenerator functions
# genre = "Truly Scary Walmart Stories"
# user_input = ""
# optimized_search_phrases ="Scary Walmart Stories", "Walmart Horror Stories"
# general_seo_phrases = "true horror stories","true scary stories", "reddit stories"
# ##########################

# ----
intro_speech_0 = f"Welcome to {genre}" #gets spoken in the intro  - DO NOT CHANGE!


lStory = []
datetime_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
# mp4_file_name = f"{datetime_string} {genre} w_music.mp4"


# helper functions
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def create_dated_folder(base_path, text_add_on):
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    folder_name = f"{datetime_string}_{text_add_on}"
    new_folder_path = os.path.join(base_path, folder_name)

    # Create the folder
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder created: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")
    return new_folder_path


#################################
# Create folder for output
cwd_path = os.getcwd()
xp_path_0 = "C:\\my\\__youtube\\videos"
additional_text = genre  # Replace with your desired text
xp_path = create_dated_folder(xp_path_0, additional_text + "_compilation")
#xp_path = r"C:\my\__youtube\videos\2024-04-13_2052_Truly Scary Walmart Stories_compilation"


for j in range(1, num_stories + 1):
    story_lib, error_list = story_gen.story_generator(
        story_type = story_type,
        genre = genre, 
        user_input = user_input)
    lStory.append([story_lib, error_list])
    print(f'''\n####################Story {j} finished''')


story_paths = [item[0] for item in lStory] # list of story libraries 
error_list = [item[1] for item in lStory] # error list from story_generator 

# manaually create lStory
# lStory = [r"C:\my\__youtube\videos\2024-04-13_2053_Truly Scary Walmart Stories",
#           r"C:\my\__youtube\videos\2024-04-13_2109_Truly Scary Walmart Stories",
#           r"C:\my\__youtube\videos\2024-04-13_2126_Truly Scary Walmart Stories",
#           r"C:\my\__youtube\videos\2024-04-13_2142_Truly Scary Walmart Stories",
#           r"C:\my\__youtube\videos\2024-04-13_2159_Truly Scary Walmart Stories",
#           r"C:\my\__youtube\videos\2024-04-13_2216_Truly Scary Walmart Stories",
#           r"C:\my\__youtube\videos\2024-04-13_2231_Truly Scary Walmart Stories"]
# story_paths = [item for item in lStory]
# lStory.append([r'C:\my\__youtube\videos\2024-03-14_1251_True Scary Tinder Dating Stories', []])

import pickle
# pickle backup of story paths
path_pickl_list = os.path.join(xp_path, "list_paths.pkl")
with open(path_pickl_list, 'wb') as file:
    # Serializing and saving lists
    pickle.dump((story_paths), file)

# Restore pickle backup
# with open(path_pickl_list, 'rb') as file:
#     story_paths = pickle.load(file)




############## concat intro and stories ####
# create intro mp4
intro_0 = intro_speech_0 + ". [pause] "
sub_text = "Smash like and subscribe to tread the thin line between reality and the surreal. Let’s begin our eerie expedition. [pause]"
intro_speech = intro_0 + sub_text


#create intro mp4 clip - creates the intro of the video - using an image from the folder xp_path
import tools_create_mp4_intro as tcmi

tcmi.create_intro_mp4(gender='male', xp_path=xp_path, story = intro_speech, fn="000_intro"  )
intro_clip = [os.path.join(xp_path, "clip_0_intro.mp4")]


######## concat stories #####
file_paths = [path + "\\clip_1.mp4" for path in story_paths]
mp4_clips =  intro_clip + file_paths
# mp4_clips = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".mp4")]
# mp4_clips = ['C:\\my\\__youtube\\videos\\2024-04-13_2053_Truly Scary Walmart Stories\\clip_1.mp4', 'C:\\my\\__youtube\\videos\\2024-04-13_2109_Truly Scary Walmart Stories\\clip_1.mp4']

print(mp4_clips)
output_concat_mp4 = os.path.join(xp_path, "" + genre + ".mp4")
start_times = tcm.concatenate_videos(mp4_clips, output_concat_mp4)

start_times_str = "Stories " + " ".join(start_times)  # to insert in top of desc

# Manual concat
# man_mp4_clips = ['C:\\my\\__youtube\\videos\\2024-03-17_0139_True Scary Tinder Dating Stories_compilation\\clip_0_intro.mp4',r"C:\my\__youtube\videos\2024-03-17_0139_True Scary Tinder Dating Stories_compilation\concat_stories_music_0.mp4"]
# man_output_concat_mp4 = os.path.join(xp_path, "concat_stories " + genre + "_music.mp4")
# concatenate_videos(man_mp4_clips, man_output_concat_mp4)


###########################
# Adding music sound track
###########################
import tools_add_music_to_mp4 as am

## add music
# output_final_mp4 = output_concat_mp4
output_final_mp4_music = os.path.join(xp_path, genre + "_music.mp4")
am.add_ambient_music_to_video(
    video_file_path=output_concat_mp4,
    music_folder_path='C:\\my\\__youtube\\videos\\horror_music',
    output_file_path=output_final_mp4_music,
    music_volume=0.02  # Adjust volume as needed
    )

###### add rain
# output_final_mp4_rain = os.path.join(xp_path, genre + "_rain.mp4")
am.add_rain_to_video(video_file_path = output_concat_mp4, music_volume=0.05)



################
#### create desc
################

#get description for all the stories
desc_stories = ""
for xp in story_paths:
    d_ = open_file(os.path.join(xp, "Stories - desc_ 1.txt"))
    # print(d_)
    desc_stories = desc_stories + d_ + "------------------\n"
# print(desc_stories)


import tools_query_chatbot as tqc
system_role="You are a helpful assistant and a worldclass writer of seo optimized descriptions for youtube"
userinput = f'''1. Create a seo and youtube search optimized description to youtube for this compilation of {genre} Horror Stories. \nDescription of the individual stories: {desc_stories}. \nUse mark down and emojies. 
I want you to optimize in order to rank #1 on google for these phrases: {optimized_search_phrases}. 
2. Go thru the description line by line and note what to optimize in order to rank #1 on google for these phrases: {optimized_search_phrases}. Rewrite it and implement the changes.
3. Go thru the desc again line by line and make sure to use these search phrases at least 10 times each in the desc: {optimized_search_phrases}.  If not then add  some text to implement it where it makes sense.
4. Output only the final and latest optimized description.\n------------'''

r = tqc.chatgpt(userinput, system_role=system_role)
desc = r.choices[0].message.content

descx = start_times_str + "\n" + desc
path_desc = os.path.join(xp_path, "desc.txt")
save_file(path_desc, str(descx))
print(descx)

# desc = open_file(path_desc)



