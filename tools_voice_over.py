#pip install Pillow
# pip install pydub
import re
import os
import openai
from openai import OpenAI
from time import time,sleep
import datetime


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
        

###########
openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)

chatbot_role = open_file("chatbot_role.txt")
chatbot_artist_role = open_file("chatbot_artist_role.txt")

break_line = "\n" + 50*"-" + "\n"

# models
# gpt4 = "gpt-4-1106-preview"
gpt4 = "gpt-4o"
gpt3 = "gpt-3.5-turbo-1106"

#chatbot
def chatgpt3 (userinput, temperature=0.8, frequency_penalty=0.2, presence_penalty=0, system_role=chatbot_role, model = gpt3):
    messagein = [
        {"role": "user", "content": userinput },
        {"role": "system", "content": system_role}]
    response = client.chat.completions.create(
        model = model,
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messagein
    )
    text = response.choices[0].message.content
    return response

##################
#   VOICE OVER   #
##################
import os
from moviepy.editor import AudioFileClip, concatenate_audioclips

def split_text(text, max_length=4096):
    """
    Splits the text into chunks, each of maximum length `max_length`.
    Tries to split at sentence ends for natural sounding speech.
    """
    words = text.split()
    current_chunk = []
    for word in words:
        if len(' '.join(current_chunk + [word])) > max_length:
            yield ' '.join(current_chunk)
            current_chunk = [word]
        else:
            current_chunk.append(word)
    yield ' '.join(current_chunk)
from moviepy.editor import AudioFileClip, concatenate_audioclips


def text2mp3(text_string="testing", voice_name="onyx", fn="output"):
    text_string = "   " + text_string
    if len(text_string) <= 4096:
        # Process the entire text if it's shorter than 4096 characters
        speech_file_path = f"{fn}.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice_name,
            input=text_string
        )
        response.stream_to_file(speech_file_path)
    else:
        # Split and process the text in chunks
        audio_clips = []
        temp_files = []
        for index, text_chunk in enumerate(split_text(text_string)):
            speech_file_path = f"{fn}_{index}.mp3"
            temp_files.append(speech_file_path)
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice_name,
                input=text_chunk
            )
            response.stream_to_file(speech_file_path)
            audio_clip = AudioFileClip(speech_file_path)
            audio_clips.append(audio_clip)

        # Concatenate audio clips
        concatenated_audio = concatenate_audioclips(audio_clips)
        concatenated_audio.write_audiofile(fn + ".mp3")

        # Close the clips and delete temporary files
        for clip in audio_clips:
            clip.close()

        for file_path in temp_files:
            os.remove(file_path)
# Example usage
# text2mp3(text_string="Your long text here...", voice_name="shimmer", fn="Lullaby")

# story = open_file('gpt_story.txt')
            
# path_voice = os.path.join(xp_path, fn + " - " + str(story_no))
# text2mp3(text_string = story, voice_name = sel_voice, fn=path_voice )
# audio_file = path_voice + ".mp3"
# count_words(story)

# text2mp3(text_string="Your long text here...", voice_name="shimmer", fn="Lullaby")

# write a function where i can test how the voice is working with different inputs. Output the mp3 file
# in this folder: "C:\my\__youtube\videos\Horror_stories_test"
def test_voice_over(text_string="testing", voice_name="onyx", fn="output"):
    """
    Tests the voice-over functionality with the given text, voice name, and output filename.

    Args:
        text_string (str): The text to be converted to speech.
        voice_name (str): The name of the voice to use.
        fn (str): The filename for the output MP3 file.
    """

    # Create the output directory if it doesn't exist
    output_dir = "C:\\my\\__youtube\\videos\\Horror_stories_test"
    os.makedirs(output_dir, exist_ok=True)

    # Generate the MP3 file
    text2mp3(text_string, voice_name, os.path.join(output_dir, fn))

    # Print a success message
    print(f"MP3 file created: {os.path.join(output_dir, fn)}.mp3")

# Example usage
# # time stamps in brackets are not said --- [08:38]  but text like [DO NOT SAY THIS] is
# test_text = '''[08:38] quaint gathering with my friends had taken a curious turn when [DO NOT SAY THIS] Mia always Enchanted by the Arcane had Unearthed the board from the attic. [08:45] just for fun she had claimed yet as everyone took their places around the ancient board I couldn't shake off a for booting sense of dread as if compelled by an unseen Force we all delicately placed our fingers on the old wooden planchet the candl light flickered casting Eerie Shadows that seemed to play tricks on our eyes is there anyone here with us Mia asked with a mixture of
# '''

# test_text ="it spelled E  -  L  -  I  -  A  -  S."
# test_voice_over(text_string=test_text, voice_name="onyx", fn="test_output")
