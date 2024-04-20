
import os
from tools_create_mp4_delete import *
from time import time,sleep
import datetime

path_0 = r"C:\my\__youtube\videos\2024-03-11_True Walmart Horror Stories_vol_2"
xp_path = os.path.normpath(path_0)

# genre = "occultism"
genre = "Walmart"
# genre = "Childhood Stories"
# genre = "Airbnb"
# genre = "ouija"
# genre = "Home Alone"

intro_0 = "Welcome to 3 scary Walmart stories that will haunt you." + " [pause] "
sub_text = "Smash like and subscribe to tread the thin line between reality and the surreal. Let’s begin our eerie expedition. "
intro_speech = intro_0 + sub_text

titles_str = '''
**Title:** "The Unseen Aisles: Trapped in Walmart's Labyrinth"
**Title:** "Endless Aisles: The Walmart That Warped Reality"
**Title:** Echoes in Aisle Nine
'''

optimized_search_phrases =''"Walmart Horror Stories",
general_seo_phrases = "Horror stories","true scary stories", "scary stories","true stories"


# //----------------------------------------------//

datetime_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
mp4_file_name = f"{datetime_string} {genre} w_music.mp4"

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)



############## concat intro and stories ####
#create intro mp4 clip
import tools_create_mp4_intro as tcmi
tcmi.create_intro_mp4(gender='male', xp_path=xp_path, story = intro_speech, fn="000_intro"  )


######## concat stories #####
mp4_clips = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".mp4")]
print(mp4_clips)
output_concat_mp4 = os.path.join(xp_path, "concat_stories.mp4")
concatenate_videos(mp4_clips, output_concat_mp4)



###########################
# Adding music sound track
###########################
import tools_add_music_to_mp4 as am

## add music
# output_final_mp4 = output_mp4
output_final_mp4_music = os.path.join(xp_path, mp4_file_name)
am.add_ambient_music_to_video(
    video_file_path=output_concat_mp4,
    music_folder_path='C:\\my\\__youtube\\videos\\horror_music',
    output_file_path=output_final_mp4_music,
    music_volume=0.05  # Adjust volume as needed
    )

###### add rain
am.add_rain_to_video(video_file_path = output_concat_mp4,music_volume=0.09)



################
#### create desc

import tools_query_chatbot as tqc
system_role="You are a helpful assistant with a knac for seo descriptions for youtube"
userinput = f'''1. Create a seo and youtube search optimized description to youtube for this compilation of {genre} Horror Stories. \nTitles: {titles_str}. \nUse mark down and emojies.  
2. Go thru the desc line by line and optimize it to rank #1 on google for these phrases: {general_seo_phrases}
3. Go thru the desc again line by line another time and make sure to use these search phrases at least 10 times each in the desc: {optimized_search_phrases}
4. Output only the description from 3). \n------------'''

r = tqc.chatgpt(userinput, system_role=system_role)
desc = r.choices[0].message.content

path_desc = os.path.join(xp_path, "desc.txt")
save_file(path_desc, str(desc))
print(desc)




