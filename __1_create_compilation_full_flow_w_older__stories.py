import os
import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
import tools_create_mp4_intro as tcmi
import tools_add_music_to_mp4 as am
import tools_query_chatbot as tqc
import tools_create_mp4 as tcm

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

def select_story_folders(base_path, compilation_length, length_type):
    all_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    
    filtered_folders = apply_filters(base_path, all_folders)
    
    # Sort folders by date (newest first)
    filtered_folders.sort(key=lambda x: datetime.datetime.strptime(x[:10], "%Y-%m-%d"), reverse=True)
    
    selected_folders = []
    total_duration = 0
    story_count = 0
    
    for folder in filtered_folders:
        clip_path = os.path.join(base_path, folder, "clip_1.mp4")
        
        with VideoFileClip(clip_path) as clip:
            duration = clip.duration
        
        if length_type == 'time' and total_duration + duration > compilation_length * 60:
            break
        elif length_type == 'count' and story_count >= compilation_length:
            break
        
        selected_folders.append(folder)
        total_duration += duration
        story_count += 1
    
    print(f"Selected {story_count} stories with a total duration of {total_duration/60:.2f} minutes")
    return selected_folders, total_duration

def apply_filters(base_path, folders):
    filtered = folders[:]
    
    filtered = [f for f in filtered if is_valid_timestamp_prefix(f)]
    filtered = [f for f in filtered if has_valid_clip(base_path, f)]
    
    return filtered

def is_valid_timestamp_prefix(folder_name):
    try:
        datetime.datetime.strptime(folder_name[:10], "%Y-%m-%d")
        return True
    except ValueError:
        return False

def has_valid_clip(base_path, folder_name):
    clip_path = os.path.join(base_path, folder_name, "clip_1.mp4")
    if not os.path.exists(clip_path):
        return False
    
    try:
        with VideoFileClip(clip_path) as clip:
            return clip.duration > 360  # 6 minutes
    except Exception as e:
        print(f"Error processing {clip_path}: {e}")
        return False



def main():
    # Configuration
    genre = "Scary Stories For Sleep"
    title_compilation = f"{genre} with Rain Sounds | True Horror Stories | Fall Asleep Quick"
    optimized_search_phrases = ["Scary Stories with Rain Sounds", "Sleep Stories with Rain Sounds", "Fall Asleep Quick"]
    general_seo_phrases = ["Sleep Stories", "ASMR rain", "Horror Stories"]

    # Define intro images for different genres
    intro_images = {
        "Scary Stories For Sleep": r"C:\my\__youtube\videos\horror_effects\intro - ScaryStoriesForSleep_7.png",
        "True Reddit Scary Stories": r"C:\path\to\reddit_scary_intro.png",
        "Truly Scary Ouija Stories": r"C:\path\to\ouija_scary_intro.png",
        # Add more genres and their corresponding intro image paths as needed
    }

    # # Get user input for compilation length
    length_type = 'time'
    compilation_length = 213 #213*60+33
    # length_type = input("Select compilation length by 'time' or 'count': ").lower()
    # if length_type == 'time':
    #     compilation_length = int(input("Enter desired compilation length in minutes: "))
    # elif length_type == 'count':
    #     compilation_length = int(input("Enter desired number of stories: "))
    # else:
    #     print("Invalid selection. Exiting.")
    #     return


    # Select story folders
    base_path = r'C:\my\__youtube\videos'
    selected_folders, total_duration = select_story_folders(base_path, compilation_length, length_type)

    # print(selected_folders)
    # selected_folders = ['2024-08-17_1835_Truly Scary Shifting Reality and Parallel Universe Stories', '2024-07-04_1609_Truly Scary Ouija Stories', '2024-08-17_1849_Truly Scary Shifting Reality and Parallel Universe Stories', '2024-07-08_2147_True Reddit Scary Stories', '2024-08-17_1902_Truly Scary Shifting Reality and Parallel Universe Stories', '2024-08-05_2039_True Reddit Scary Stories', '2024-08-05_2054_True Reddit Scary Stories', '2024-07-20_2243_Truly Scary Ouija Stories', '2024-07-20_2307_Truly Scary Ouija Stories', '2024-07-20_2331_Truly Scary Ouija Stories', '2024-07-10_1304_True Reddit Scary Stories',  '2024-07-08_2202_True Reddit Scary Stories', '2024-07-08_2216_True Reddit Scary Stories', '2024-07-08_2241_True Reddit Scary Stories', '2024-07-04_2005_Truly Scary Ouija Stories', '2024-07-04_2018_Truly Scary Ouija Stories']
 
    # Present selected folders for validation
    print("\nSelected folders:")
    for i, folder in enumerate(selected_folders, 1):
        print(f"{i}. {folder}")
    print(f"\nTotal duration: {total_duration/60:.2f} minutes")

    # selected_folders = [
    #     '2024-08-19_1102_Truly Scary Shifting Reality and Parallel Universe Stories',
    #     '2024-08-19_1725_ouija Scary Stories +',
    #     '2024-08-19_1703_True Reddit Scary Stories +',
    #     '2024-08-19_1709_True Reddit Scary Stories +',
    #     '2024-08-19_1712_True Reddit Scary Stories +',
    #     '2024-08-19_1726_ouija Scary Stories +',
    #     '2024-08-17_1835_Truly Scary Shifting Reality and Parallel Universe Stories',
    #     '2024-08-19_1706_True Reddit Scary Stories+',
    #     '2024-08-17_1849_Truly Scary Shifting Reality and Parallel Universe Stories',
    #     '2024-08-17_1902_Truly Scary Shifting Reality and Parallel Universe Stories',
    #     '2024-07-20_2243_Truly Scary Ouija Stories',
    #     '2024-08-05_2039_True Reddit Scary Stories',
    #     '2024-08-05_2054_True Reddit Scary Stories',
    #     '2024-07-20_2307_Truly Scary Ouija Stories',
    #     '2024-08-19_1714_ouija_Scary Stories+',
    #     '2024-07-20_2331_Truly Scary Ouija Stories',
    #     '2024-07-10_1304_True Reddit Scary Stories'
    #     ]

    # Ask for confirmation
    confirmation = input("\nDo you want to proceed with these folders? (yes/no): ").lower()
    if confirmation != 'yes':
        print("Operation cancelled. Exiting.")
        return


    # Create full paths for selected folders
    import random
    # random.shuffle(selected_folders)     # randomize order in selected_folders
    story_paths = [os.path.join(base_path, folder) for folder in selected_folders]


    # Create output folder
    xp_path_0 = r"C:\my\__youtube\videos"
    xp_path = create_dated_folder(xp_path_0, f"{genre}_compilation")

    # Get the intro image path for the current genre
    intro_image_path = intro_images.get(genre)
    if not intro_image_path or not os.path.exists(intro_image_path):
        print(f"Warning: No intro image found for genre '{genre}'. Using default image.")
        intro_image_path = r"C:\my\__youtube\videos\horror_effects\intro - ScaryStoriesDefault.png"  # Specify a default image path

    # Create intro
    # intro_speech = f'''Hello everyone, and welcome back to Horror Stories! Tonight is all about {genre}. ...'''
    # intro_speech = f'''
    # Welcome back, night owls, to Horror Stories. Tonight's {genre} selection is crafted especially for those who use our chilling tales as a macabre lullaby. We're honored to be your sinister storyteller as you drift into the realm of shadows.
    # Before you surrender to slumber, we're dying to know: **What number fills you with dread, and why does it haunt your waking hours?** Last week's responses sent shivers down our spine. Think you can outdo them? Share your numerical nightmares in the comment section below.
    # For the full bone-chilling experience, don your headphones. As you nestle into your false sense of security, remember: our stories have a habit of seeping into your subconscious...
    # If our nocturnal narratives keep you coming back for more, don't forget to like and subscribe. Your support ensures you'll never miss a spine-tingling bedtime story. Now, make yourself comfortable and steel your nerves. In the twisted world of our tales, the boundary between sleep and waking terrors is unsettlingly blurred. Pleasant dreams... if you dare to have them. And may your cursed number stay far from tonight's horrors.
    # '''
    intro_speech = f'''Welcome back to Horror Stories. Tonight's {genre} tale is perfect for those who like to fall asleep to our scary stories. We're happy to be your creepy bedtime companion as you drift off to sleep.
     Before you close your eyes, we want to ask: **What number scares you, and why?** Last week's answers were really interesting. Think you can top them? Tell us about your scary numbers in the comments below. 
     For the best experience, use headphones. As you get comfy, remember: our stories might follow you into your dreams... 
     If you're enjoying our nightly stories, please like and subscribe. This way, you won't miss any of our scary bedtime tales. Now, get ready. In our stories, sleep and nightmares are very close. Sweet dreams... if you can have them. And we hope your unlucky number stays away from tonight's scares.
     '''

    # intro_speech = f'''Welcome back to Horror Stories. Tonight's {genre} edition is tailor-made for those of you who use our tales as a dark lullaby. We're pleased to be your eerie sleep companion as you drift off to our whispers in the night.
    # Before you close your eyes, we're curious: **What's your cursed number, and why does it haunt you?** Last week's responses were intriguing. Think you can top them? Share your numerical nightmares in the comments.
    # For the full immersive experience, grab your headphones. As you settle in, remember: our stories might just follow you into your dreams...
    # If you're enjoying our nocturnal narratives, don't forget to like and subscribe. Your support ensures you never miss a terrifying bedtime story. Now, get comfy and prepare yourself. In the world of our stories, the line between sleep and waking nightmares is frighteningly thin. Sweet dreams, if you can manage them... and may your unlucky number stay far from tonight's horrors.'''
    try:
        tcmi.create_intro_mp4(gender='male', xp_path=xp_path, story=intro_speech, fn="000_intro", intro_image=intro_image_path)
        intro_clip = [os.path.join(xp_path, "clip_0_intro.mp4")]
    except Exception as e:
        print(f"Error creating intro clip: {e}")
        print("Proceeding without intro clip.")
        intro_clip = []

    # logo_video = r"C:\my\__youtube\videos\horror_effects\horror video intro 6s_1080p.mp4"
    black_screen_10min_1080p = r"C:\my\__youtube\videos\horror_effects\black_screen_10min_1080p.mp4"
    # Create incite text
    incite_text = "....If you've made it this far, the shadows have already begun to close in. Subscribe now to ensure you never miss a terrifying tale. And if you dare, hit the thanks button to buy me a cup of midnight brew. Your support keeps the nightmares flowing. Now, brace yourself for our next story... [pause]"
    incite_audio_clip = tcmi.create_voice_over(gender='male', xp_path=xp_path, story=incite_text, fn="002_incite_audio")
    incite_video_path = r"C:\my\__youtube\videos\horror_effects\incite_coffee.mp4"  # Replace with actual path


    # Prepare video clips
    black_screen = [black_screen_10min_1080p] * 2

    mp4_clips = intro_clip + [os.path.join(path, "clip_1.mp4") for path in story_paths] + black_screen
    print(mp4_clips)
    # Concatenate videos
    output_concat_mp4 = os.path.join(xp_path, f"{genre}.mp4")
    end_sound_path = r"C:\my\__youtube\videos\horror_effects\Cartoon Cowbell.mp3"  # Replace with actual path if you have an end sound


    start_times = tcm.concatenate_videos(
        mp4_clips, 
        output_concat_mp4, 
        end_sound_path,
        incite_audio_path=incite_audio_clip,
        incite_video_path=incite_video_path,
        incite_position=2  # This will insert after the first story
    )

    start_times_str = "Stories " + " ".join(start_times)  # to insert in top of desc

    xp_path = r'C:\\my\\__youtube\\videos\\2024-08-25_1927_Scary Stories For Sleep_compilation'
    import tools_ffmpeg
    cut to desired length

    import pickle
    # pickle backup of story paths
    path_pickl_list = os.path.join(xp_path, "list_paths.pkl")
    with open(path_pickl_list, 'wb') as file:
        # Serializing and saving lists
        pickle.dump((mp4_clips, start_times_str), file)

# # add logo in front
# import tools_ffmpeg as tff
# logo_video = r"C:\my\__youtube\videos\horror_effects\horror video intro 6s.mp4"
# rain_10m_video = r"C:\my\__youtube\videos\sound_effects\rain and black screen 10 min.mp4"

# input_files = [logo_video, output_concat_mp4, rain_10m_video, rain_10m_video, rain_10m_video]

# # add 30 minutes of rain


    # Add rain
    am.add_rain_to_video(video_file_path=output_concat_mp4, music_volume=0.2)

    
    # Add music
    output_final_mp4_music = os.path.join(xp_path, f"{genre}_music.mp4")
    am.add_ambient_music_to_video(
        video_file_path=output_concat_mp4,
        music_folder_path=r'C:\my\__youtube\videos\horror_music\composed in suno',
        output_file_path=output_final_mp4_music,
        music_volume=0.03
    )


    # Create description
    desc_stories = ""
    for i, path in enumerate(story_paths, 1):
        desc_file = os.path.join(path, "Stories - desc_ 1.txt")
        if os.path.exists(desc_file):
            desc_stories += f"Chapter {i}: " + open_file(desc_file) + "------------------\n"
        else:
            print(f"Warning: Description file not found in {path}")

    
    system_role = "You are a helpful assistant and a worldclass writer of seo optimized descriptions for youtube"
    userinput = f'''1. Create a seo and youtube search optimized description to youtube for this compilation of {genre} Horror Stories. \nDescription of the individual stories: {desc_stories}. \nUse mark down and emojies. 
    I want you to optimize in order to rank #1 on google for these phrases: {optimized_search_phrases}. 
    2. Go thru the description line by line and note what to optimize in order to rank #1 on google for these phrases: {optimized_search_phrases}. Rewrite it and implement the changes.
    3. Go thru the desc again line by line and make sure to use these search phrases at least 2 times each in the desc: {optimized_search_phrases}.  If not then add  some text to implement it where it makes sense.
    4. Go through the text and edit it shorter than 5000 chars.
    5. Output only the final and latest optimized description.\n------------'''

    desc = tqc.chatgpt(userinput, system_role=system_role, model="gpt-4o")
    
    # Add start times to the description
    final_desc = start_times_str + "\n\n" + desc
    
    path_desc = os.path.join(xp_path, "desc.txt")
    save_file(path_desc, final_desc)
    print(final_desc)

if __name__ == "__main__":
    main()

