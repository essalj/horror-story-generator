import os
from time import time, sleep
import datetime
import tools_create_mp4 as tcm
import flow_0b_short_story_gen_assistants as story_gen
import pickle
import tools_create_mp4_intro as tcmi
import tools_add_music_to_mp4 as am
import  tools_query_chatbot as tqc
import tools_ffmpeg as tff


'''title_compilation = "7 Terrifying Tales from the Wilderness | True Camping Horror Stories! 🏕️🌲💀"
num_stories = 5
story_type = "camping"
genre = "WILDERNESS HORROR STORIES"
user_input = ""
optimized_search_phrases = "Real Camping Horror Experiences", "True Wilderness Survival Stories"
general_seo_phrases = "scary camping encounters", "middle of nowhere stories", "backwoods horror tales", "isolated camping experiences", "forest survival stories"
'''
'''title_compilation = "7 Bone-Chilling Ghost Encounters | True Paranormal Experiences! 👻🔮✨"
num_stories = 3
story_type = "ghost"
genre = "GHOST STORIES"
user_input = ""
optimized_search_phrases = "Real Ghost Encounter Experiences", "True Haunting Tales"
general_seo_phrases = "encounters with spirits", "haunted house stories", "paranormal experiences"
'''
#title_compilation = "2 Mind-Bending Reality Shifting Stories | True Multiverse Experiences! 🌌🔄✨"
#num_stories = 1
#story_type = "shifting"
##genre = "REALITY SHIFTING Stories"
#user_input = ""
#optimized_search_phrases = "Parallel Universe Shifting Experiences", "True Reality Shifting Tales"
#general_seo_phrases = "shifting to desired reality", "parallel universe stories", "multiverse experiences"
#intro_image = r"C:\my\git\__youtube\Horror Stories - audio_video_defaults\horror_stories_error_default_image.png"

# Define variables at the beginning of the script
# title_compilation = "Scary Ouija Board Horror Stories with RAIN SOUNDS to Help You FALL ASLEEP QUICK! 👻🔮🌙"
# num_stories = 1
# story_type = "Ouija"
# genre = "Truly Scary Ouija Board Stories"
# user_input = ""
# optimized_search_phrases = "Scary Ouija Board Stories", "Ouija Board Horror Stories"
# general_seo_phrases = "true horror stories", "scary stories for sleep", "reddit stories"
#intro_image = r"C:\my\__youtube\videos\Thumbnails\tn_ouija2.jpg"
# "C:\my\__youtube\videos\2024-11-25_1809_Truly Scary Ouija Board Stories_compilation\Horror thumbnails - 2024-11-25T201549.750.png"

title_compilation = "Terrifying Sheriff's Shift: True Crime Accounts 🚓🔦🎙️"
num_stories = 6
story_type = "sheriff"
genre = "Truly Scary Sheriff Shift Stories" # or "Gripping True Crime: Sheriff's Darkest Shift"
user_input = "" # This would be populated by specific user requests for a story
optimized_search_phrases = ("Scary Sheriff Stories", "True Crime Sheriff Shift", "Terrifying Police Encounter Stories")
general_seo_phrases = ("true crime", "cop stories", "sheriff stories")

# title_compilation = "8 Scary Home Alone Stories | True Disturbing Stories! 🏠😱👻"
# num_stories = 8
# story_type = "home_alone"
# genre = "SCARY Home Alone Stories"
# user_input = ""
# optimized_search_phrases = "Haunted Home Alone Horror Stories", "Terrifying Home Alone Tales"
# general_seo_phrases = "true horror stories", "scary stories for sleep", "reddit stories"
# intro_image = r"C:\my\__youtube\videos\2025-02-18_1452_SCARY Home Alone Stories_compilation\tn_will_u_play_W_me.png"

# title_compilation = "4 Scary Valentine’s Day Stories | True Disturbing Stories! 💔👻❤️"
# num_stories = 4
# story_type = "valentine"
# genre = "Sinister Valentine's Day Stories"
# user_input = ""
# optimized_search_phrases = "Haunted Valentine's Horror Stories", "Valentine's Day Horror Tales"
# general_seo_phrases = "true horror stories", "scary stories for sleep", "reddit stories"
# intro_image = r"C:\my\__youtube\videos\2025-02-14_1831_Sinister Valentine's Day Stories_compilation\a-digital-illustration-with-a-halloween-themed-val (1).jpg"

gpt4 = "gpt-4.1"  # gpt4 model selection
gpt4mini = "gpt-4.1-mini" # gpt4 model selection

# intro_speech_q = f'''You are a world class horror story writer for youtube. Please rewrite this YOUTUBE INTRO and change the theme to: {genre} .
# Make it same style and feel as the one below.
# DO NOT EXCEED 120 WORDS!
# OUTPUT NOTHING BUT THE INTRO!!
# --------------------------------------------
# Welcome to Sleep Stories and Rain, where the comfort of home turns into a stage for chilling tales of isolation and suspense. Tonight, we explore the eerie silence of being alone, where familiar walls hide unseen dangers and storms outside echo the turmoil within. Support our channel by liking and subscribing, and join a community that faces the shadows together. Share your most unsettling home-alone experiences in the comments—unexplained knocks, strange presences, or nights that changed everything. Your stories inspire us. If you crave suspense and psychological thrills, you’re in the right place. Let’s begin our first story....
# ----------------------------
# DO NOT EXCEED 120 WORDS!
# OUTPUT NOTHING BUT THE INTRO!!
# '''

# intro_text = tqc.chatgpt(userinput=intro_speech_q, system_role="You are a helpful assistant", model=gpt4)

# incite_text = ".....If you've made it this far, the shadows have already begun to close in. Subscribe now to ensure you never miss a terrifying tale. And if you dare, hit the thanks button to buy me a cup of midnight brew. Your support keeps the nightmares flowing. Now, brace yourself for our next story... [pause]"

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

def main():
    try:
        print("Starting the horror story compilation process...")

        # Create folder for output
        print("Creating output folder...")
        xp_path_0 = '/Users/lasse/Desktop/my/youtube' #mac
        #xp_path_0 = "C:\\my\\__youtube\\videos" # pc
        xp_path = create_dated_folder(xp_path_0, genre + "_compilation")
        print(f"Output folder created: {xp_path}")
        # xp_path = r"C:\my\__youtube\videos\13 ouija stories"



        ###############################
        # Create mp4 intro clips
        # print("Creating intro clip...")
        # tcmi.create_intro_mp4(gender='male', xp_path=xp_path, story=intro_text, fn="clip_000_intro", intro_image = intro_image)
        # intro_clip = os.path.join(xp_path, "clip_000_intro.mp4")

        # Scale intro clip to 1080p
        # scaled_intro_clip_list = tff.scale_videos_to_1080p([intro_clip])
        # intro_clip = scaled_intro_clip_list[0]



        # create incite clip
        # tcmi.create_intro_mp4(gender='male', xp_path=xp_path, story=incite_text, fn="clip_001_incite", intro_image = incite_image)
        # incite_clip = os.path.join(xp_path, "clip_001_incite.mp4")

        # list mp4_story clips


        p0 = "/Users/lasse/Desktop/my/Git/horror_story_trimmed/generated_stories"

        # mp4_story_paths = [path + "\\clip_1.mp4" for path in story_paths]
        # mp4_story_paths = [os.path.join(xp_path, f"{fn}.mp4") for fn in base_filenames]
        mp4_story_paths = [os.path.join(p0, f) for f in os.listdir(p0) if f.lower().endswith('.mp4')]

        
        ########## default clips
        intro_mp4_logo = r"C:\my\__youtube\videos\horror_effects\1024p\horror video intro 5s_scaled_1024p.mp4"
        end_sound_mp4 = r"C:\my\__youtube\videos\horror_effects\1024p\Cartoon Cowbell_1024p_scaled.mp4"
        silence_2s_mp4 = r"C:\my\__youtube\videos\horror_effects\1024p\silence_2s_1024p.mp4"
        rain60m = r"C:\my\__youtube\videos\horror_effects\1024p\black screen_rain_60min_1024p_scaled.mp4"
        
        #f = r"C:\my\__youtube\videos\horror_effects\Cartoon Cowbell_1080p.mp4"
        #scale mp4
        #tff.scale_videos_to_1080p([rain60m], width=1792, height=1024)

        ############## concat files
        i1 = [intro_mp4_logo, intro_clip]
        i2 = [mp4_story_paths[0], incite_clip]
        i3 = [item for sublist in [[end_sound_mp4, item] for item in mp4_story_paths[1:]] for item in sublist]

        i_all = i1 + i2 + i3 + [rain60m]*3
#        i_all = ['C:\\my\\__youtube\\videos\\horror_effects\\1024p\\horror video intro 5s_scaled_1024p.mp4','C:\\my\\__youtube\\videos\\2025-05-04_2009_WILDERNESS HORROR STORIES_compilation\\clip_000_intro.mp4', 'C:\\my\\__youtube\\videos\\2025-05-04_2009_WILDERNESS HORROR STORIES\\clip_1.mp4', 'C:\\my\\__youtube\\videos\\2025-05-04_2009_WILDERNESS HORROR STORIES_compilation\\clip_001_incite.mp4', 'C:\\my\\__youtube\\videos\\horror_effects\\1024p\\Cartoon Cowbell_1024p_scaled.mp4', 'C:\\my\\__youtube\\videos\\2025-05-04_2025_WILDERNESS HORROR STORIES\\clip_1.mp4'] + [rain60m]
        #o1 = os.path.join(xp_path, "_concat_1.mp4")
        #o2 = os.path.join(xp_path, "_concat_2.mp4")
        #o3 = os.path.join(xp_path, "_concat_3.mp4")
        o_all = os.path.join(xp_path, "_raw_t_video.mp4")

        #tcm.concat_mp4(input_files=input_files,output_file=_concat_4)
    #    tff.concat_mp4(i1, o1)
     #   tff.concat_mp4(i2, o2)
      #  tff.concat_mp4(i3, o3)
        tff.concat_mp4(i_all, o_all)
        

        #tff.concatenate_videos_ffmpeg_demuxer(i1, o1)
        #tff.concatenate_videos_ffmpeg_demuxer(i2, o2)

'''
        # Concatenate story videos
        print("Concatenating videos...")
        incite_video_path = r"C:\my\__youtube\videos\horror_effects\incite_coffee.mp4"
        start_times = tcm.concatenate_videos_plus(
            mp4_clips,
            output_concat_mp4,
            end_sound_path,
            incite_audio_path=incite_audio_clip,
            incite_video_path=incite_video_path,
            incite_position=2
        )

        start_times_str = "Stories " + " ".join(start_times)
'''

        # add rain to story
#        fn_out = am.add_rain_to_video(video_file_path=output_concat_mp4, music_volume=0.14)


         #add tn anim in fromt of video
 
 
        # Cut final video
        print("Cutting final video...")
        tff.cut_video(output_file_t1, output_file_rain_x, start_time="00:00:00", duration="06:06:05.51")

        # Create description
        print("Creating description...")
        desc_stories = open_file(os.path.join(xp_path, "stories_text.txt"))
        # for xp in story_paths:
        #     d_ = open_file(os.path.join(xp, "Stories - desc_ 1.txt"))
        #     desc_stories = desc_stories + d_ + "------------------\n"

        system_role = "You are a helpful assistant and a worldclass writer of seo optimized descriptions for youtube"
        userinput = f'''1. Create a seo and youtube search optimized description to youtube for this compilation of {genre} Horror Stories.
        Include what is said about the story format here: {intro_speech} \nDescription of the individual stories: {desc_stories}. \nUse mark down and emojies.
        I want you to optimize in order to rank #1 on google for these phrases: {optimized_search_phrases}.
        2. Go thru the description line by line and note what to optimize in order to rank #1 on google for these phrases: {optimized_search_phrases}. Rewrite it and implement the changes.
        3. Go thru the desc again line by line and make sure to use these search phrases at least 10 times each in the desc: {optimized_search_phrases}.  If not then add  some text to implement it where it makes sense.
        4. Go through the text and edit it shorter than 5000 chars.
        5. Output only the final and latest optimized description.\n------------'''


        r = tqc.chatgpt(userinput, system_role=system_role, model=gpt4)
        # r = tqc.chatgpt(userinput, system_role=system_role, model=gpt4)
        desc = r

        descx = start_times_str + "\n" + desc
        path_desc = os.path.join(xp_path, "desc.txt")
        save_file(path_desc, str(descx))
        print("Description saved: /n" + descx)

        print("Process completed successfully!")
except Exception as e:
    print(f"An error occurred during the compilation process: {e}")

if __name__ == "__main__":
    main()

