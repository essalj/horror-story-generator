
import os
import tools_create_mp4 as tcm
from time import time, sleep
import datetime
import _1_short_story_gen_assistants as story_gen


# ##########################
# ##### Shifting Reality Stories
# title_compilation = "TRUE Scary Shifting Reality Stories"
# num_stories = 12
# story_type = "shifting"  # controls the storygenerator functions
# genre = "Truly Scary Shifting Reality and Parallel Universe Stories"
# user_input = ""
# optimized_search_phrases = "Scary Shifting Reality Stories", "Parallel Universe Horror Stories"
# general_seo_phrases = "true horror stories", "true scary stories", "reddit stories"
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


# # ##########################
# # ##### Tinder/dating Stories
# title_compilation = "TRUE Scary Dating Stories"
# num_stories = 12
# story_type = "tinder" # controls the storygenerator functions
# genre = "Truly Scary tinder online dating Stories"
# user_input = ""
# optimized_search_phrases ="Scary Tinder Dating Stories", "Tinder Dating Horror Stories"
# general_seo_phrases = "true horror stories","true scary stories", "reddit stories"
# # # ##########################


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

# ###########################
# ############# Reddit scary stories
title_compilation = "TRUE Scary Stories From Reddit | Dark Tales with Rain Ambience for Sleep"
num_stories = 3
story_type = "Reddit" # controls the storygenerator functions
genre = "True Reddit Scary Stories"
user_input = ""
optimized_search_phrases = "Scary Stories with Rain Sounds", "Creepy Reddit Stories for Sleep"
general_seo_phrases = "scary stories for sleep", "ASMR rain", "reddit horror stories for bedtime"
##########################

# ###########################
# # ############# ouija stories
# title_compilation = "TRUE Scary ouija board Stories From The Internet | True Scary Stories"
# num_stories = 5
# story_type = "Ouija" # controls the storygenerator functions
# genre = "Truly Scary Ouija Stories"
# user_input = ""
# optimized_search_phrases ="Scary Ouija Board Stories", "Ouija Board Horror Stories"
# general_seo_phrases = "true horror stories","scary stories for sleep", "reddit stories"
# # ##########################

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

gpt4 = "gpt-4o" # gpt4 model selection
# intro_speech_0 = f"Welcome to {genre}" #gets spoken in the intro  - DO NOT CHANGE!
intro_speech = f'''Hello everyone, and welcome back to Horror Stories! Tonight is all about {genre}.  I know a lot of you use these videos to sleep so before you drift off into the world of darkness, share your unlucky number and the spooky story behind it! Is it 13, or does 666 give you the chills? We'd love to hear what number haunts you and why. And if you're enjoying our nightly journeys into the realm of darkness and horrors, don't forget to like and subscribe. It helps our haunted community grow and ensures you never miss a spine-tingling episode. Now, let's get comfy and relaxed as we begin tonight's tales. Grab your headphones for the best immersive experience, and if you're using this to sleep, sweet dreams... If you have an Ouija board nearby, maybe keep it closed... just in case! Stay tuned, and sleep tight... you never know what numbers might appear in your dreams tonight!'''


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

# Get the list of matching folders
def list_folders(base_path, prefix):
    folders = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and d.startswith(prefix)]
    return folders
# folders = list_folders(base_path = "C:\\my\\__youtube\\videos",prefix = "2024-06-11")
# for folder in folders:
#     print(folder)

# ['C:\\my\\__youtube\\videos\\2024-06-05_1311_Truly Scary Shifting Reality and Parallel Universe Stories', 'C:\\my\\__youtube\\videos\\2024-06-05_1312_Truly Scary Shifting Reality and Parallel Universe Stories', 'C:\\my\\__youtube\\videos\\2024-06-05_1329_Truly Scary Shifting Reality and Parallel Universe Stories', 'C:\\my\\__youtube\\videos\\2024-06-05_1345_Truly Scary Shifting Reality and Parallel Universe Stories', 'C:\\my\\__youtube\\videos\\2024-06-05_1401_Truly Scary Shifting Reality and Parallel Universe Stories', 'C:\\my\\__youtube\\videos\\2024-06-05_1419_Truly Scary Shifting Reality and Parallel Universe Stories', 'C:\\my\\__youtube\\videos\\2024-06-05_1435_Truly Scary Shifting Reality and Parallel Universe Stories', 'C:\\my\\__youtube\\videos\\2024-06-05_1453_Truly Scary Shifting Reality and Parallel Universe Stories']

#################################
# Create folder for output
cwd_path = os.getcwd()
xp_path_0 = "C:\\my\\__youtube\\videos"
additional_text = genre  # Replace with your desired text
xp_path = create_dated_folder(xp_path_0, additional_text + "_compilation")
#xp_path = r'C:\\my\\__youtube\\videos\\2024-07-04_1609_Truly Scary Ouija Stories_compilation'

for j in range(1, num_stories + 1):
    story_lib, error_list = story_gen.story_generator(
        story_type = story_type,
        genre = genre, 
        user_input = user_input)
    lStory.append([story_lib, error_list])
    print(f'''\n####################Story {j} finished''')


story_paths = [item[0] for item in lStory] # list of story libraries 
error_list = [item[1] for item in lStory] # error list from story_generator 

# lStory.append([r'C:\my\__youtube\videos\2024-03-14_1251_True Scary Tinder Dating Stories', []])
# story_paths = [r'C:\\my\\__youtube\\videos\\2024-07-20_2243_Truly Scary Ouija Stories', r'C:\\my\\__youtube\\videos\\2024-07-20_2255_Truly Scary Ouija Stories']


import pickle
# pickle backup of story paths
path_pickl_list = os.path.join(xp_path, "list_paths.pkl")
with open(path_pickl_list, 'wb') as file:
    # Serializing and saving lists
    pickle.dump((story_paths), file)

# Restore pickle backup
# with open(path_pickl_list, 'rb') as file:
#     story_paths = pickle.load(file)


# concatenate  files "Stories - story 1.txt" from all the dirs in story_path to a file
stories_str = "\n".join([open_file(os.path.join(path, "Stories - story 1.txt")) for path in story_paths])
path_desc = os.path.join(xp_path, "stories_text.txt")
save_file(path_desc, str(stories_str))


############## concat intro, incite_text  and stories ####
# create intro mp4 clip - creates the intro of the video - using an image from the folder xp_path
import tools_create_mp4_intro as tcmi
tcmi.create_intro_mp4(gender='male', xp_path=xp_path, story = intro_speech, fn="000_intro"  )
intro_clip = [os.path.join(xp_path, "clip_0_intro.mp4")]


# #create incite text - incites listener to subscribe and buy me a cup of mocca
incite_text = ".....If you've made it this far, the shadows have already begun to close in. Subscribe now to ensure you never miss a terrifying tale. And if you dare, hit the thanks button to buy me a cup of midnight brew. Your support keeps the nightmares flowing. Now, brace yourself for our next story... [pause]"
incite_audio_clip = tcmi.create_voice_over(gender='male', xp_path = xp_path, story = incite_text, fn="002_incite_audio")
incite_video_path = r"C:\my\__youtube\videos\horror_effects\incite_coffee.mp4"  # Replace with actual path



######## concat stories #####
file_paths = [path + "\\clip_1.mp4" for path in story_paths]
mp4_clips =  intro_clip + file_paths
# mp4_clips = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".mp4")]
# 2024-05-11: include  mp4_clips = ['C:\\my\\__youtube\\videos\\2024-05-11_0916_Truly Scary Ouija Stories_compilation\\clip_0_intro.mp4', 'C:\\my\\__youtube\\videos\\2024-05-11_0001_Truly Scary Ouija Stories\\clip_1.mp4', 'C:\\my\\__youtube\\videos\\2024-05-11_0018_Truly Scary Ouija Stories\\clip_1.mp4', 'C:\\my\\__youtube\\videos\\2024-05-11_0035_Truly Scary Ouija Stories\\clip_1.mp4', 'C:\\my\\__youtube\\videos\\2024-05-11_0050_Truly Scary Ouija Stories\\clip_1.mp4', 'C:\\my\\__youtube\\videos\\2024-05-11_0105_Truly Scary Ouija Stories\\clip_1.mp4']

print(mp4_clips)
output_concat_mp4 = os.path.join(xp_path, "" + genre + ".mp4")


# concatenate_videos(video_files, output_path, end_sound_path=None, incite_audio_path=None, incite_video_path=None, incite_position=2)
# When calling concatenate_videos
start_times = tcm.concatenate_videos(
    mp4_clips, 
    output_concat_mp4, 
    end_sound_path,
    incite_audio_path=incite_audio_clip,
    incite_video_path=incite_video_path,
    incite_position=2  # This will insert after the first story
)


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
    music_volume=0.03  # Adjust volume as needed
    )

###### add rain
# output_final_mp4_rain = os.path.join(xp_path, genre + "_rain.mp4")
am.add_rain_to_video(video_file_path = output_concat_mp4, music_volume=0.28)



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
4. Go through the text and edit it shorter than 5000 chars.
5. Output only the final and latest optimized description.\n------------'''

r = tqc.chatgpt(userinput, system_role=system_role, model=gpt4)
desc = r

descx = start_times_str + "\n" + desc
path_desc = os.path.join(xp_path, "desc.txt")
save_file(path_desc, str(descx))
print(descx)

