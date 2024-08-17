import pandas as pd
from gtts import gTTS
from PIL import Image
import requests
from io import BytesIO
import moviepy.editor as mp
# from transformers import pipeline

def create_dataframe(text_file):
    with open(text_file, 'r') as file:
        lines = file.readlines()
    df = pd.DataFrame({'text': lines})
    df['word_count'] = df['text'].apply(lambda x: len(x.split()))
    return df

def generate_image_prompt(text):
    summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", max_length=30)
    prompt = summarizer(text)[0]['summary_text']
    return prompt

def get_image(prompt):
    # Placeholder for image generation API call
    # For now, we'll use a placeholder image
    response = requests.get(f"https://via.placeholder.com/800x600.png?text={prompt}")
    return Image.open(BytesIO(response.content))

def text_to_speech(text, filename):
    tts = gTTS(text)
    tts.save(filename)
    return filename

def create_video_clip(image_file, audio_file, duration):
    audio = mp.AudioFileClip(audio_file)
    image = mp.ImageClip(image_file).set_duration(duration)
    return image.set_audio(audio)

def main(text_file, output_file):
    df = create_dataframe(text_file)
    df['image_prompt'] = df['text'].apply(generate_image_prompt)
    
    clips = []
    for index, row in df.iterrows():
        image = get_image(row['image_prompt'])
        image_file = f"image_{index}.png"
        image.save(image_file)
        
        audio_file = f"audio_{index}.mp3"
        text_to_speech(row['text'], audio_file)
        
        clip = create_video_clip(image_file, audio_file, row['word_count'] / 2)  # Assuming 2 words per second
        clips.append(clip)
    
    final_clip = mp.concatenate_videoclips(clips)
    final_clip.write_videofile(output_file, fps=24)

if __name__ == "__main__":
    main("input_text.txt", "output_video.mp4")

    