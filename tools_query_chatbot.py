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

# Get key for openai
# openai_api_key = userdata.get('openai')
# openai.api_key = open_file('openaiapikey.txt')
openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
client = OpenAI(api_key=openai_api_key)

###############
# Definitions
###############

# chatbot_role = open_file("chatbot_role.txt")
# chatbot_artist_role = open_file("chatbot_artist_role.txt")
break_line = "\n" + 50*"-" + "\n"

# models
gpt4 = "gpt-4-1106-preview"
gpt3 = "gpt-3.5-turbo-1106"

#chatbot
def chatgpt(userinput, system_role="You are a helpful assistant", model = gpt4, temperature=0.8, frequency_penalty=0.2, presence_penalty=0):
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
# chatgpt(userinput, system_role="You are a helpful assistant", model = gpt4, temperature=0.8, frequency_penalty=0.2, presence_penalty=0)


#####################################

