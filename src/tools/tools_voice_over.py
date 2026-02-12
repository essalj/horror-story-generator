#pip install Pillow
# pip install pydub
# pip install moviepy
 
import re
import os
import openai
from openai import OpenAI
from time import time,sleep
import datetime
from moviepy import AudioFileClip, ColorClip, CompositeVideoClip, concatenate_audioclips
 
 
# os.getcwd()
 
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
 
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)
        
 
###########
openai_api_key = open_file('/Users/lasse/Desktop/my/Git/api-keys/openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)
 
chatbot_role = open_file("chatbot_role.txt")
chatbot_artist_role = open_file("chatbot_artist_role.txt")
os.getcwd()
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
 
 
def text2mp3(text_string="testing", model="tts-1", voice_name="onyx", fn="output"):
    text_string = "   " + text_string
    if len(text_string) <= 4096:
        # Process the entire text if it's shorter than 4096 characters
        speech_file_path = f"{fn}.mp3"
        response = client.audio.speech.create(
            model=model,
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
                model=model,
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
    
 
 
 
def test_voice_over(text_string="testing", model="tts-1-hd", voice_name="onyx", fn="output"):
    """
    Tests the voice-over functionality with the given text, voice name, and output filename.
 
    Args:
        text_string (str): The text to be converted to speech.
        voice_name (str): The name of the voice to use.
        fn (str): The filename for the output MP3 file.
    """
 
    # Create the output directory if it doesn't exist
    output_dir = "/Users/lasse/Desktop/my/youtube/videos/Test_Stories"
    os.makedirs(output_dir, exist_ok=True)
 
    # Generate the MP3 file
    fn = os.path.join(output_dir, fn)
    text2mp3(text_string=text_string, model=model, voice_name=voice_name, fn=fn)
 
    # Print a success message
    print(f"MP3 file created: {os.path.join(output_dir, fn)}.mp3")
 
 
def convert_folder_to_mp3(input_folder, output_folder, model="tts-1-hd", voice_name="onyx"):
    """
    Converts all .txt files in the input folder to MP3 files using the text2mp3 function.
 
    Args:
        input_folder (str): Path to the folder containing .txt files.
        output_folder (str): Path to the folder where MP3 files will be saved.
        model (str): The TTS model to use.
        voice_name (str): The name of the voice to use.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
 
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            # Construct full file paths
            input_file_path = os.path.join(input_folder, filename)
            output_file_name = os.path.splitext(filename)[0]  # Remove .txt extension
            output_file_path = os.path.join(output_folder, output_file_name)
 
            # Read the text file
            with open(input_file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
 
            print(f"Converting {filename} to MP3...")
 
            # Convert text to MP3
            text2mp3(text_string=text_content, model=model, voice_name=voice_name, fn=output_file_path)
 
            print(f"Converted {filename} to {output_file_name}.mp3")
 
    print("All files processed.")
 
def convert_mp3_to_192kbps(input_file_path, output_file_path=None):
    """
    Converts an existing MP3 file to 192 kbps bitrate.
    
    Args:
        input_file_path (str): Path to the input MP3 file.
        output_file_path (str, optional): Path for the output MP3 file. If None, 
                                          will use the original filename with '_192kbps' suffix.
    
    Returns:
        str: Path to the converted MP3 file.
    """
    # Import required libraries
    from pydub import AudioSegment
    
    # Create output path if not provided
    if output_file_path is None:
        file_name, file_ext = os.path.splitext(input_file_path)
        output_file_path = f"{file_name}_192kbps{file_ext}"
    
    # Load the audio file
    print(f"Loading audio file: {input_file_path}")
    audio = AudioSegment.from_mp3(input_file_path)
    
    # Export with the specified bitrate
    print(f"Converting to 192 kbps and saving to: {output_file_path}")
    audio.export(output_file_path, format="mp3", bitrate="192k")
    
    print(f"Conversion complete: {output_file_path}")
    return output_file_path
 
def convert_folder_mp3_to_192kbps(input_folder, output_folder=None):
    """
    Converts all MP3 files in a folder to 192 kbps.
    
    Args:
        input_folder (str): Path to the folder containing MP3 files.
        output_folder (str, optional): Path to save the converted files. If None,
                                      files will be saved in the input folder with '_192kbps' suffix.
    """
    # Create output folder if provided
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
    
    # Process all MP3 files in the folder
    count = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.mp3'):
            input_path = os.path.join(input_folder, filename)
            
            if output_folder:
                output_path = os.path.join(output_folder, filename)
            else:
                output_path = None  # Function will create path with _192kbps suffix
            
            convert_mp3_to_192kbps(input_path, output_path)
            count += 1
    
    print(f"Converted {count} MP3 files to 192 kbps")
 
 
 
#ex.
#story = open_file('/Users/lasse/Desktop/my/youtube/videos/2025-05-19 cop stories/cop_story_01.txt')
#text2mp3(text_string=story, model="tts-1", voice_name="onyx", fn="output")
