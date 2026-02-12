##################
# FLOW:
#     tools_json_2_mp4.py
#     _1_create_compilation_from_files.py 


import os
import time # Import the time module
import tools_json_extract_story_and_img as tj
import tools_voice_over as tvo
import tools_query_chatbot as tqc
import sys
import tools_create_images as tci


# user settings
json_path = '/Users/lasse/Desktop/my/youtube/videos/2025-05-29 cop stories'
intro_image = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/police_car_1024p.png'
incite_image = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/1024p/police_car_1024p.png'

title_compilation = "Scary Sheriff & Cop Horror Stories with RAIN SOUNDS to Help You FALL ASLEEP QUICK! 🚓🌧️😱"
#num_stories = 1
story_type = "sheriff"
genre = "Truly Scary Police and Sheriff Stories"

json_files = [os.path.join(json_path, f) for f in os.listdir(json_path) if f.lower().endswith('.json')]
# 0,1,2,6 - en af hver model

############
gpt4 = "gpt-4.1"  # gpt4 model selection

####################
# Create images
####################
def create_images(images):
    image_files = []
    image_error_path = "/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/cemetary1024p.png"
    for i in range(0, len(images)):
        img_prompt0 = str(images[i])        
        print(i, "orig prompt:\n ",img_prompt0, "\n ---------------------")
        #i=3
        #improve image prompt
        img_prompt = tci.improve_image_prompt(img_prompt0)         
        print("improved prompt:\n ", img_prompt, "\n ---------------------")

        path_img = fn_ + "-img_" + str(i)
        
        try:  #if no image or if problem with image then reuse the former
            image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn= path_img)
            image_files.append(filename)
            # Renaming logic is now handled after this call
        except:   
            try:
                qq = f"This prompt was declined by Dall-e. Please rephrase it  carefully, so it passes the filters in Dall-e: {img_prompt}.... AGAIN MAKE SURE TO OUTPUT NOTHING BUT THE PROMPT"
                img_prompt2 = tqc.chatgpt(userinput=qq, system_role="You are a helpful assistant", model=gpt4)
                print(qq, "-----------", img_prompt2)
                
                image_url, filename = tci.chatgpt_dalle(prompt = img_prompt2, fn= path_img)
                print(image_url, filename)
                image_files.append(filename)
            except:
                if i>=1:
                    image_files.append(image_files[-1])
                else:
                    image_files.append(image_error_path)
                    error_list.append(f"Error_default_image in position {i} in function create_images()")

    return image_files

#json_files[4]
# filename = '/Users/lasse/Desktop/my/youtube/videos/2025-05-19 cop stories/cop_story_07.json'
def main():
    for i in range(0, len(json_files)):
        filename = json_files[i]
        filename_without_extension, _ = os.path.splitext(filename)
        fn_ = filename_without_extension
        print(fn_)

        story, images, gender, path, fn = tj.extract_story_and_prompts(filename)


        #decide gender of narrator
        q_narrator = "Read thru the story and decide if the main character is male or female. Answer only 'male' or 'female', nothing else.....\n------\n" + story + "\n----------\nDecide if the main character is male or female. Answer only 'male' or 'female', nothing else....."
        search_term = tqc.chatgpt(userinput=q_narrator, system_role="You are a helpful assistant", model=gpt4)
        voice = "onyx"
        if "female" in search_term.lower():
            voice = "shimmer"
        print(voice)


        # create mp3
        tvo.text2mp3(text_string=story, model="tts-1", voice_name=voice, fn=fn_)
        #fn_mp3=os.path.join(path,fn)


        #create images
        image_files = create_images(images)
        #image_files = '/Users/lasse/Desktop/my/youtube/videos/2025-05-19 cop stories/cop_story_03-img_0_20250524_090520.png' '/Users/lasse/Desktop/my/youtube/videos/2025-05-19 cop stories/cop_story_03-img_1_20250524_090548.png' '/Users/lasse/Desktop/my/youtube/videos/2025-05-19 cop stories/cop_story_03-img_4_20250524_090707.png' '/Users/lasse/Desktop/my/youtube/videos/2025-05-19 cop stories/cop_story_03-img_5_20250524_090735.png' '/Users/lasse/Desktop/my/youtube/videos/2025-05-19 cop stories/cop_story_03-img_6_20250524_090815.png'


        #create mp4
        import tools_create_mp4 as tcm4
            
        fn_mp3 = fn_ + ".mp3" # Set audio_file to the result of MP3 creation
        fn_mp4 = fn_ + ".mp4"
        #  def create_mp4(output_mp4):
        tcm4.create_video_with_images_and_audio(image_paths=image_files, audio_path=fn_mp3, output_filename=fn_mp4, fps=30)


