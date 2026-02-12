import os

# xp_path = os.getcwd()
# xp_path = r"C:\my\__youtube\videos\2024-03-11_True Walmart Horror Stories_vol_2"


####################
# Create voice over
####################
import tools_voice_over as tvo
def create_voice_over(gender = 'male', xp_path = "", story = "Scary stories", fn = "000_intro"):
    path_voice = os.path.join(xp_path, fn)

    search_term = "female"
    if search_term.lower() in gender.lower():
        gender = "female"
    else:
        gender = "male"

    if gender=="female":
        voice = "shimmer"
    else:
        voice = "onyx"
    tvo.text2mp3(text_string = story, voice_name = voice, fn=path_voice )
    audio_file = path_voice + ".mp3"
    return audio_file

# audio_file = create_voice_over(gender='male', xp_path = x_path_0, story = "3 Horror stories that will haunt you", fn="000_intro")
# audio_files = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".mp3")]
# audio_file = audio_files[0]

##############################################
#### create mp4 - images and voice
# image_files[]  -   image list for story
# story  - text for current story
# audiofile - current story voice over
# story_no -  current story no.
#   
##############################################
from tools_create_mp4 import *

# image_files = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".png")]
# image_file = image_files[0]
def create_mp4(output_mp4, image_files, audio_file):
    create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)
    


def create_intro_mp4(gender='male', xp_path="", story="Horror stories that will haunt you.", fn="000_intro", intro_image=None):
    audio_file = create_voice_over(gender=gender, xp_path=xp_path, story=story, fn=fn)
    
    if intro_image and os.path.exists(intro_image):
        image_files = [intro_image]
    else:
        image_files = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".png")]
        
        if not image_files:
            image_files = [r"C:\my\__youtube\Horror Stories - audio_video_defaults\horror_stories_error_default_image.png"]
        return
    
    output_final_mp4 = os.path.join(xp_path, fn + ".mp4")
    
    create_mp4(output_mp4=output_final_mp4, image_files=image_files, audio_file=audio_file)
# create_intro_mp4(gender='male', xp_path=xp_path, story = "3 Scary Walmart stories that will haunt you. Volume 2", fn="000_intro"  )




       # tcmi.create_intro_mp4(gender='male', xp_path=xp_path, story=intro_text, fn="clip_000_intro", intro_image = intro_image)
