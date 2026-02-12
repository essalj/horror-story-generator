
import os


## MODELS
# writer_model = 'anthropic/claude-opus-4.6'
writer_model = 'moonshotai/kimi-k2.5'
worker_model = 'google/gemini-2.5-flash'
import tools_query_openrouter as tqo

import tools_file_operations
import random

import flow_1c_yt_description_generator as desc_gen
import flow_1a_create_mp4_story as story_mp4_gen
import flow_1b_create_compilation_from_files as compilation_gen

# test_run = 0
# test_run = 1

def get_genre(user_story_query):
    # Get story genre from user input
    if len(user_story_query)<5:
        user_story_query = "I want a scary ouija board story"

    # define genre
    q_story_type = "u r a world class fiction writer. Figure out what story type the user is asking for. It can be 'ouija story', 'trucker story', 'sheriff story', 'cop story' ... or any type u think, but no more than 2 words. I want nothing but the story type as output - NO MORE THAN 2 WORDS. This is the user input: " + str(user_story_query)
    genre = tqo.query_openrouter(prompt=q_story_type, model=worker_model)
    print(genre)
    return genre


def select_old_stories(old_stories=0):
    old_story_path = []
    if old_stories>=1:
        path0 = '/Users/lasse/Desktop/my/youtube'
        story_list = tools_file_operations.find_ouija_stories(path0 = path0, search="", filter="compil")
        random.shuffle(story_list)
        old_story_path = story_list[0:old_stories]
    return old_story_path
#select_old_stories(3)

qq

def run_full_flow(new_stories, old_stories, user_story_query, genre, rain_hours):
    """
    Orchestrates the full flow of generating stories, compiling MP4s, and generating YouTube assets.

    Args:
        new_stories (int): The number of stories to generate.
        user_story_query (str): The base query for generating stories.
        genre (str): The genre of the stories (e.g., "Ouija Board", "Sheriff").
        title_compilation (str): The title for the compilation video.
        rain_hours (int): The number of hours of rain sound to add to the compilation.
    """
    genre = get_genre(user_story_query)
    title = genre + " with RAIN SOUNDS to Help You FALL ASLEEP QUICK! 🌧️😱" # Title for the compilation
    print(f"Starting full flow for {new_stories+old_stories} stories of genre '{genre}' with {rain_hours} hours of rain...")

    if old_stories>0:
        old_story_path = select_old_stories(old_stories)
        print(old_story_path)
    else:
        old_story_path = []

    mp4_story_paths = []
    if new_stories>=1:
        for i in range(new_stories):
            print(f"\nGenerating story {i+1}/{new_stories}...")
            # Generate individual story MP4s
            # The generate_story_mp4 function in flow_1a_create_mp4_story.py determines the genre internally
            # based on the user_story_query. We'll pass the base query.
            story_mp4_path = story_mp4_gen.generate_story_mp4(user_query=user_story_query, model=writer_model)
            if story_mp4_path:
                mp4_story_paths.append(story_mp4_path)
            else:
                print(f"Failed to generate MP4 for story {i+1}. Skipping.")

    if not mp4_story_paths:
        print("No stories were successfully generated. Exiting.")
        return

    print("\nAll individual stories generated. Starting compilation...")
    # Compile individual story MP4s into one

# all_stories_path = ['/Users/lasse/Desktop/my/youtube/2025-09-17_2307_ouija story_story/2025-09-17_230757-ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-09-17_2208_ouija story_story/2025-09-17_220949-ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-09-17_2012_ouija story_story/2025-09-17_201353-ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-09-17_2006_ouija story_story/2025-09-17_200705-ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-09-17_1958_ouija story_story/2025-09-17_195924-ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-09-17_1953_ouija story_story/2025-09-17_195358-ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-08-02_1758 ouija story/2025-08-02_175912-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-08-04_2330 ouija story/2025-08-04_233104-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-09-10_1550_ouija story_story/2025-09-10_155141-ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-09-10_1543_ouija story_story/2025-09-10_154439-ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-01_2153_Ouija Horror_story/2025-07-01_215404-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-08-04_2249 ouija story/2025-08-04_224951-Ouija Horror.mp4']

    all_stories_path = mp4_story_paths + old_story_path
    # Save all_stories_path to a file for recovery if job fails
    with open('all_stories_path.txt', 'w') as f:
        for path in all_stories_path:
            f.write(path + '\n')
    compiled_mp4_path, bookmarks, xp_path = compilation_gen.create_compilation_mp4(all_stories_path, genre, rain_hours)


    if not compiled_mp4_path:
        print("Failed to create compilation MP4. Exiting.")
        return

    print(f"\nCompilation MP4 created: {compiled_mp4_path}")
    print(f"Output folder: {xp_path}")
    print(f"Generated Bookmarks:\n{bookmarks}")

    print("\nGenerating YouTube description and posts...")
    # Generate YouTube description
    yt_description = desc_gen.generate_youtube_description(genre=genre, title=genre, bookmarks=bookmarks)
    print("\n--- YouTube Description ---")
    print(yt_description)


    
    # Generate Community Post
    community_post_1 = desc_gen.generate_community_post(genre)
    print("\n--- Community Post 1 ---")
    print(community_post_1)


    # Generate Reminder Post (using it as the second community post for now)
    community_post_2 = desc_gen.generate_reminder_post(genre)
    print("\n--- Community Post 2 ---")
    print(community_post_2)

    # Save the generated content to files
    desc_gen.save_generated_content(xp_path, yt_description, community_post_1, community_post_2)

    print("\nFull flow completed successfully!")

if __name__ == "__main__":
    # Example Usage:
    new_stories = 2  # Number of new stories to generate
    old_stories = 0 # Number of old stories to include
    # story_query = "True scary story from reddit" # Base query for the stories
    # compilation_genre = "Disturbing True scary story from reddit" # Genre for the compilation
    # compilation_title = "Disturbing True scary story from reddit with RAIN SOUNDS to Help You FALL ASLEEP QUICK! 🌧️😱" # Title for the compilation
    # story_query = "Scary Shrink story about a devious and manipultaing shrink - NO SUPERNATURAL STUFF" # Base query for the stories
    # compilation_genre = "Disturbing True Shrink Horror" # Genre for the compilation
    # compilation_title = "Disturbing True Shrink Horror with RAIN SOUNDS to Help You FALL ASLEEP QUICK! 🌧️😱" # Title for the compilation
    # story_query = "True Scary Trucker Horror"
    # user_story_query = "Scary Xmas Horror story for adults"
    user_story_query = "Appalaichian trail horror story" # Base query for the stories
    # user_story_query = "Disturbing True Ouija Horror Stories" # Base query for the stories   rain_hours = 1 # Number of hours of rain to add
    rain_hours =1

    # run_full_flow(new_stories, old_stories, user_story_query, genre, rain_hours)


# mp4_story_paths = 
# ['/Users/lasse/Desktop/my/youtube/2025-07-30_2303 ouija Story/2025-07-30_230416-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-30_2327 ouija Story/2025-07-30_232817-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-30_2342 ouija Story/2025-07-30_234343-ouija Story.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-30_2310 ouija Story/2025-07-30_231053-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-30_2335 ouija Story/2025-07-30_233602-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-30_2318 ouija Story/2025-07-30_231849-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-30_2254 ouija Story/2025-07-30_225505-Horror Story.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-02_1615_Ouija Horror_story/2025-07-02_161612-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-02_1636_Ouija Horror_story/2025-07-02_163658-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-02_1258_Ouija Horror_story/2025-07-02_125851-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-02_1307_Ouija Horror_story/2025-07-02_130745-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-02_1538_Ouija Horror_story/2025-07-02_154012-Ouija Horror.mp4']

'''
['/Users/lasse/Desktop/my/youtube/2025-07-30_2335 ouija Story/2025-07-30_233602-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-08-06_2149 ouija story/2025-08-06_215000-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-08-04_2241 ouija story/2025-08-04_224152-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/videos/2025-05-17_2308_Truly Scary Ouija Board Stories/clip_1.mp4', '/Users/lasse/Desktop/my/youtube/2025-09-03_2308_ouija story_story/2025-09-03_230913-ouija story.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-20_1838_ouija/2025-07-20_183835-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-30_2303 ouija Story/2025-07-30_230416-Ouija Horror.mp4', '/Users/lasse/Desktop/my/youtube/2025-07-30_2327 ouija Story/2025-07-30_232817-Ouija Horror.mp4']
'''

#mp4_story_paths=['/Users/lasse/Desktop/my/youtube/2025-09-10_1559_ouija story_story/2025-09-10_160018-ouija story.mp4','/Users/lasse/Desktop/my/youtube/2025-09-10_1550_ouija story_story/2025-09-10_155141-ouija story.mp4','/Users/lasse/Desktop/my/youtube/2025-09-10_1543_ouija story_story/2025-09-10_154439-ouija story.mp4','/Users/lasse/Desktop/my/youtube/2025-09-10_1536_ouija story_story/2025-09-10_153732-ouija story.mp4','/Users/lasse/Desktop/my/youtube/2025-09-10_1036_ouija story_story/2025-09-10_103731-ouija story.mp4']
