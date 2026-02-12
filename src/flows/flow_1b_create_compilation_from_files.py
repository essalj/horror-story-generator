##################
# # FLOW 1:
# #     

import os
from time import time, sleep
import datetime
import tools_create_mp4 as tcm
import flow_0b_short_story_gen_assistants as story_gen
import pickle
import tools_create_mp4_intro as tcmi
import tools_add_music_to_mp4 as am
import tools_query_chatbot as tqc
import tools_ffmpeg as tff
import json
import tools_voice_over as tvo

import moviepy as mp


# # json_path = '/Users/lasse/Desktop/my/youtube/videos/2025-05-25 cop stories'

# # title_compilation = "Scary Sheriff & Cop Horror Stories with RAIN SOUNDS to Help You FALL ASLEEP QUICK! 🚓🌧️😱"
# # #num_stories = 1
# # story_type = "sheriff"
# # genre = "Truly Scary Police and Sheriff Stories"


# # title_compilation = "Scary Ouija Boards Stories with RAIN SOUNDS to Help You FALL ASLEEP QUICK! 🚓🌧️😱"
# # #num_stories = 17
# # story_type = "ouija"
# # genre = "Truly Scary Ouija Board experinces"


gpt4 = "gpt-4.1"  # gpt4 model selection
# gpt4mini = "gpt-4.1-mini" # gpt4 model selection

def create_intro_speech_mp4(genre, xp_path, intro_image):
    # genre = "Scary true story about encounter w big bear, lion, wolf in the wilderness"

    intro_speech_q = f'''You are a world class horror story writer for youtube. Please rewrite this YOUTUBE INTRO and change the theme to: {genre}.
    Make it same style and feel as the one below. Add something like 50% IS SUBSCRIBED...pls subscribe
    DO NOT EXCEED 120 WORDS!
    OUTPUT NOTHING BUT THE INTRO!!
    --------------------------------------------
    Welcome to Sleep Stories and Rain, where the comfort of home turns into a stage for chilling tales of isolation and suspense. Tonight, we explore the eerie silence of being alone, where familiar walls hide unseen dangers and storms outside echo the turmoil within. Support our channel by liking and subscribing, and join a community that faces the shadows together. Share your most unsettling home-alone experiences in the comments—unexplained knocks, strange presences, or nights that changed everything. Your stories inspire us. If you crave suspense and psychological thrills, you’re in the right place. Let’s begin our first story....
    ----------------------------
    DO NOT EXCEED 120 WORDS!
    OUTPUT NOTHING BUT THE INTRO!!
    '''

    intro_text = tqc.chatgpt(userinput=intro_speech_q, system_role="You are a helpful assistant", model=gpt4)
    tcmi.create_intro_mp4(gender='male', xp_path=xp_path, story=intro_text, fn="000_intro", intro_image=intro_image)

# xp_path = '/Users/lasse/Desktop/my/youtube/2025-07-08_1150_Trucker horror stories_compilation'
#  '/Users/lasse/Desktop/my/youtube/2025-07-02_2205_Scary true story about encounter w big bear, lion, wolf etc. no supernatural stuff_compilation'
# path_voice = os.path.join(xp_path, "intro" )
# model = "tts-1"  #or "tts-1-hd"
# tvo.text2mp3(text_string = intro_text, model=model, voice_name = "onyx", fn=path_voice )
# audio_file = path_voice + ".mp3"
# audio_file = '/Users/lasse/Desktop/my/youtube/2025-07-02_2205_Scary true story about encounter w big bear, lion, wolf etc. no supernatural stuff_compilation/intro.mp3'

# incite_text = ".....If you've made it this far, the shadows have already begun to close in. Subscribe now to ensure you never miss a terrifying tale. And if you dare, hit the thanks button to buy me a cup of midnight brew. Your support keeps the nightmares flowing. Now, brace yourself for our next story... [pause]"
#intro_speech = 
#mp4_story_paths = ['/Users/lasse/Desktop/my/youtube/2025-07-02_2142_Wilderness Survival_story/2025-07-02_214306-Wilderness Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-02_2150_Wilderness Survival_story/2025-07-02_215137-Wilderness Survival.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-02_2158_Wilderness Survival_story/2025-07-02_215930-Wilderness Survival.mp4']

# Helper functions
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

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder created: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")
    return new_folder_path


def get_duration_mp4(file_path):
    """Gets the duration of an MP4 file using moviepy."""
    try:
        clip = mp.VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def create_bookmarks(video_paths):
    """
    Calculates the duration of video clips and generates a bookmark string.

    Args:
        video_paths (list): A list of paths to the video files.

    Returns:
        str: The generated bookmark string.
    """
    results = []
    for file_path in video_paths:
        duration = get_duration_mp4(file_path)
        if duration is not None:
            filename = os.path.basename(file_path)  # Extract filename
            results.append((duration, filename))

    def format_duration(seconds):
        """Converts seconds to HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    running_sum = 0
    no_ = 0
    output_string = "" # Initialize an empty string to store the output
    for n, r in enumerate(results):
        ts_ = r[0]
        fn_ = r[1]
        running_sum += ts_
        formatted_ts = format_duration(running_sum)
        if ts_ > 30:
            no_ += 1
            output_string += f"{formatted_ts} - Story {no_}\n" # Append to the string

    return output_string


# genre = "Trucker horror stories"
# path0 = '/Users/lasse/Desktop/my/youtube'
# [os.path.join(root, d) for root, dirs, _ in os.walk(path0) for d in dirs if "trucker" in d.lower()]

## mp4 - list w criteria of mp4 ouija story files
    # import tools_file_operations
    # path0 = '/Users/lasse/Desktop/my/youtube'
    # ouija_story_paths = tools_file_operations.find_ouija_stories(path0 = path0, search="2025-07-02")

# o1 = ouija_story_paths
# o2= ouija_story_paths
# mp4_story_paths = o1 + o2
# mp4_story_paths = ouija_story_paths
# #mp4_story_paths = [os.path.join(root, file) for root, _, files in os.walk(path0) for file in files if file.lower().endswith(".mp4") and os.path.getsize(os.path.join(root, file)) > (12 * 1024 * 1024)]


# mp4_story_paths = ['/Users/lasse/Desktop/my/youtube/2025-07-20_1805 ouija/2025-07-20_180626-Ouija Horror.mp4','/Users/lasse/Desktop/my/youtube/2025-07-20_1838_ouija/2025-07-20_183835-Ouija Horror.mp4','/Users/lasse/Desktop/my/youtube/2025-07-20_2138_ouija/2025-07-20_213912-Horror Story.mp4','/Users/lasse/Desktop/my/youtube/2025-07-20_1854_ouija/2025-07-20_185433-Ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-02_1615_Ouija Horror_story/2025-07-02_161612-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-06-20_0152_Ouija Story_compilation/2025-06-20_015254-Ouija Story.mp4', '/Users/lasse/Desktop/my/youtube/2025-06-19_1732_Ouija Story/2025-06-19_173326-Ouija story.mp4']

# import random
# randomize = 1
# mp4_story_paths = (lambda lst: random.sample(lst, len(lst)) if randomize == 1 else lst)([os.path.join(root, file) for root, _, files in os.walk(path0) for file in files if file.lower().endswith(".mp4") and 12 * 1024 * 1024 < os.path.getsize(os.path.join(root, file)) < 65 * 1024 * 1024])


#mp4_story_paths =['/Users/lasse/Desktop/my/youtube/2025-07-05_0946_Trucker Horror_story/2025-07-05_094751-Trucker Horror.mp4','/Users/lasse/Desktop/my/youtube/2025-07-05_0939_Trucker Horror_story/2025-07-05_094002-Trucker Horror.mp4','/Users/lasse/Desktop/my/youtube/2025-07-05_0931_Trucker Horror_story/2025-07-05_093156-Trucker Horror.mp4']
def create_compilation_mp4(mp4_story_paths, genre, rain_hours=1):
    try:
        print("Starting the horror story compilation process...")

        # Create folder for output
        print("Creating output folder...")
        xp_path_0 = '/Users/lasse/Desktop/my/youtube' #mac
        #xp_path_0 = "C:\\my\\__youtube\\videos" # pc
        xp_path = create_dated_folder(xp_path_0, genre + "_compilation")

        print(f"Output folder created: {xp_path}")
        
        # Define intro_image with a default value
        intro_image = None 

        ########## default clips - mac
        end_sound_mp4 = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/heart_beat_3s_1024p_scaled.mp4'
        silence_2s_mp4 = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/silence_2s_1024p.mp4'
        rain60m = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/black screen_rain_60min_1024p_scaled.mp4'
       
        #ntro_mp4 based on genre
        if "ouija" in genre.lower():
            intro_image = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/ouija_intro_image.png'
            incite_image = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/ouija_incite_image.png'
            intro_mp4 = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/ouija intro 2_1024p.mp4'
        elif "police" in genre.lower() or "sheriff" in genre.lower():
            intro_image = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/police_car_1024p.png'
            incite_image = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/police_car_1024p.png'
            intro_mp4 = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/intro_police_story_1024p_scaled.mp4'
        elif "woods" in genre.lower() or "forest" in genre.lower():
            intro_image = '/Users/lasse/Desktop/my/youtube/tn images/tn_wilderness_predator1_1024p.webp'
            incite_image = '/Users/lasse/Desktop/my/youtube/tn images/tn_wilderness_predator2.webp'
            intro_mp4 = '/Users/lasse/Desktop/my/youtube/Horror Stories - audio_video_defaults/intro_predator_nature_1024p_scaled.mp4'
        
        elif "trucker" in genre.lower():
            intro_image = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/trucker_1024p.png'
            incite_image = intro_image
            intro_mp4 = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/horror video intro 5s_scaled_1024p.mp4'
        
        
        else:
            # Default intro if genre not matched
            intro_image = '/Users/lasse/Desktop/my/youtube/tn images/tn_wilderness_predator1_1024p.webp'
            incite_image = '/Users/lasse/Desktop/my/youtube/tn images/tn_wilderness_predator2.webp'
            intro_mp4 = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/horror video intro 5s_scaled_1024p.mp4'
        

        create_intro_speech_mp4(genre, xp_path, intro_image)
        intro_speech_mp4 = os.path.join(xp_path, "000_intro.mp4")

        #rain_hours = 3
        ############## concat files
        try:    
            i1 = [intro_speech_mp4]
        except: 
            i1 = [intro_mp4]
        i2 = [end_sound_mp4, mp4_story_paths[0]]
        i3 = [item for sublist in [[end_sound_mp4, item] for item in mp4_story_paths[1:]] for item in sublist]
        i_all = i1 + i2 + i3 + [rain60m]*rain_hours
        o_all = os.path.join(xp_path, "_raw_t_video.mp4")

        success, attempted_files = tff.concat_mp4(i_all, o_all)
        if success:
            print("stories: " + str(len(mp4_story_paths)))
            print("\n--- Concatenation Overview ---")
            print("Successfully concatenated the following files:")
            for f in attempted_files:
                print(f"- {f}")
            print("------------------------------")
        else:
            print("\n--- Concatenation Overview ---")
            print("Failed to concatenate the following files:")
            for f in attempted_files:
                print(f"- {f}")
            print("------------------------------")

        bookmarks = create_bookmarks(i_all)
        return o_all, bookmarks, xp_path

    except Exception as e:
        print(f"An error occurred during compilation: {e}")
        return None, None, None
