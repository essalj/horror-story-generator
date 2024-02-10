import os
from openai import OpenAI
from dotenv import load_dotenv
from colorama import Fore

"""
Variation of Current API Calling Format as of 12/26/23
"""
load_dotenv()
try:
    client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY']
        )
    if not client.api_key:
        raise ValueError("API key is missing. Check .env file.")
except KeyError as e:
    raise ValueError(f"Error Occurred: {e}\n\nCheck .env file.")
print(Fore.GREEN + f'API KEY: {client.api_key}')


# thread_id = 'thread_YourThread123'
thread_id = thread.id
output_path = '/path/to/your/output/file'


"""
Obtain the File IDs within the Specified Thread
"""
def get_response(thread_id):
    return client.beta.threads.messages.list(thread_id=thread_id)

def get_file_ids_from_thread(thread):
    file_ids = [
        file_id
        for m in get_response(thread)
        for file_id in m.file_ids
    ]
    return file_ids
file_ids = get_file_ids_from_thread(thread)

"""
Write Each File ID's Contents with Separator Implementation for Readability
"""
def write_file(file_id, count, output_path=output_path):
    file_data = client.files.content(file_id) # Extract the content from the file ID
    file_content = file_data.read() # Assign the content to a variable
    separator_start = f'\n\n\n\nFILE # {count + 1}\n\n\n\n'
    separator_end = '\n\n\n\n' + '#' * 100 + '\n\n\n\n'

    with open(output_path, "ab") as file:
        file.write(separator_start.encode())  # Encode the string to bytes
        file.write(file_content) # Write the content
        file.write(separator_end.encode())    # Encode the string to bytes


"""
Iterate through the File IDs while Calling write_file for File Output
"""
file_ids = get_file_ids_from_thread(thread_id) # Retrieve file IDs
print('\nFILE IDS: ', file_ids)
print('\nNUMBER OF FILE IDS: ', len(file_ids))
for count, file_id in enumerate(file_ids):
    print(Fore.GREEN + f'\nWriting file #{count + 1}...\n')
    write_file(file_id, count) # Write file ID contents
    print(Fore.GREEN + f'File {count + 1} written.\n')

print('Done.')