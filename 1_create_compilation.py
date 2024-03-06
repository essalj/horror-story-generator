
import os
from create_mp4 import *
from time import time,sleep
import datetime

# genre = "occultism"
# genre = "Walmart"
# genre = "Childhood Stories"
# genre = "Airbnb"
genre = "ouija"
# genre = "Home Alone"
datetime_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
mp4_file_name = f"{datetime_string} {genre} w_music.mp4"

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


path_0 = r"C:\my\__youtube\videos\2024-03-05_True Ouija Board Horror Stories compilation - vol2"
xp_path = os.path.normpath(path_0)
mp4_clips = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".mp4")]

print(mp4_clips)

output_concat_mp4 = os.path.join(xp_path, "compilation.mp4")

concatenate_videos(mp4_clips, output_concat_mp4)


################
#### create desc

# titles = [file.replace(".mp4", "", 1) for file in os.listdir(xp_path) if file.endswith(".mp4")]
# titles_str = '\n'.join(titles)
titles_str = '''
**Title**: "Whispers Beyond the Veil: A Pact with Shadows"
**Title:** Shadows of Desire: The Ouija Board Pact
**Title:** Whispering Shadows: The Asylum's Untold Legacy

'''


import tools_query_chatbot as tqc
system_role="You are a helpful assistant with a knac for seo descriptions for youtube"
userinput = '''Create a seo and youtube search optimized description to youtube for this compilation of ''' + genre + ''' Horror Stories
Titles: ''' + titles_str + '''\n Use mark down and emojies.''' 

r = tqc.chatgpt(userinput, system_role=system_role)
desc = r.choices[0].message.content
path_desc = os.path.join(xp_path, "desc.txt")
# desc2 = desc.choices[0].message.content
save_file(path_desc, str(desc))
# chatgpt(userinput, system_role="You are a helpful assistant", model = gpt4, temperature=0.8, frequency_penalty=0.2, presence_penalty=0)

print(desc)


###########################
# Adding music sound track
###########################
import add_music_to_mp4 as am

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




