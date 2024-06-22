
import os
import openai
from openai import OpenAI
import json

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Initialize OpenAI API
openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
# openai.api_key = openai_api_key
client = OpenAI(api_key=openai_api_key)

gpt4 = "gpt-4o"

# # Chatbot function
# def chatgpt(userinput, system_role="You are a helpful assistant", model=gpt4, temperature=0.8, frequency_penalty=0.2, presence_penalty=0):
#     messages = [
#         {"role": "system", "content": system_role},
#         {"role": "user", "content": userinput}
#     ]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=temperature,
#         frequency_penalty=frequency_penalty,
#         presence_penalty=presence_penalty
#     )
#     text = response.choices[0].message['content']
#     return text

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
    return text

