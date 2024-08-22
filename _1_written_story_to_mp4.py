
import os
import tools_json_to_image as tjti


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    

## Create voice over
import tools_voice_over as tvo
def create_voice_over(story, xp_path, gender = "Male"):
    fn = "voice_over"
    path_voice = os.path.join(xp_path, fn)
    search_term = gender  #"female"
    if search_term.lower()=="female":
        voice = "shimmer"
    else:
        voice = "onyx"
    print(gender, voice)
    tvo.text2mp3(text_string = story, model ="tts-1-hd", voice_name = voice, fn=path_voice )
    audio_file = path_voice + ".mp3"
    return audio_file
# audio_file = create_voice_over(gender)


## Create mp4
import tools_create_mp4 as tcm4 


# fn_story_text = r"C:\my\__youtube\videos\2024-08-19_1102_Truly Scary Shifting Reality and Parallel Universe Stories - v2\claude_20240817_glitch-in-the-matrix-story.md"
# fn_json = r"C:\my\__youtube\videos\2024-08-19_1102_Truly Scary Shifting Reality and Parallel Universe Stories - v2\glitch-in-the-matrix-analysis.json"

def create_mp4_from_story(xp_path, fn_story_text, fn_json):
    fn_json = os.path.join(xp_path, fn_json)
    fn_story_text = os.path.join(xp_path, fn_story_text)
    story = open_file(fn_story_text)
    gender = "Male"

    image_files = tjti.create_images_from_json(fn_json, xp_path)
    audio_file = create_voice_over(story=story, xp_path=xp_path, gender = "Male")

    output_mp4 = os.path.join(xp_path, "clip_1" + ".mp4")
    tcm4.create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)



# xp = r"C:\my\__youtube\videos\2024-08-19_1709_True Reddit Scary Stories +-"
# xp2 = r"C:\my\__youtube\videos\2024-08-19_1712_True Reddit Scary Stories +-"
# xp3 = r"C:\my\__youtube\videos\2024-08-19_1724_ouija Scary Stories +-"
# xp4 = r"C:\my\__youtube\videos\2024-08-19_1706_True Reddit Scary Stories+-"

# audio_file = os.path.join(xp_path, "voice_over.mp3")
# image_files = [os.path.abspath(os.path.join(xp_path, f)) for f in os.listdir(xp_path) if f.lower().endswith('.png')]



# create_mp4_from_story(xp_path=xp, fn_story_text = "story.txt", fn_json="story_json.json")
# create_mp4_from_story(xp_path=xp2, fn_story_text = "story.txt", fn_json="story_json.json")
# create_mp4_from_story(xp_path=xp4, fn_story_text = "story.txt", fn_json="story_json.json")
