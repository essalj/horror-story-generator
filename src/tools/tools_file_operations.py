

import os
from time import time, sleep
import datetime

# Helper functions
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def create_dated_folder(base_path, text_add_on):
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    folder_name = f"{datetime_string}_{text_add_on}"
    new_folder_path = os.path.join(base_path, folder_name)

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder created: {new_folder_path}")
    else:
        print(f"Folder already exists: {new_folder_path}")
    return new_folder_path


def find_ouija_stories(path0 = '/Users/lasse/Desktop/my/youtube', search="", filter=""):

    
    mp4_story_paths = []
    for root, _, files in os.walk(path0):
        if "ouija" in root.lower() and search.lower() in root.lower() and (len(filter)>1 and filter not in root.lower()):
            # Find all qualifying MP4 files in this directory
            mp4_files = [
                file for file in files
                if file.lower().endswith(".mp4")
                and (15 * 1024 * 1024) < os.path.getsize(os.path.join(root, file)) < (90 * 1024 * 1024)
            ]

            # If there are MP4 files, get the largest one
            if mp4_files:
                largest_file = max(mp4_files, key=lambda f: os.path.getsize(os.path.join(root, f)))
                mp4_story_paths.append(os.path.join(root, largest_file))

    print(str(len(mp4_story_paths)) + " stories found.")
    return mp4_story_paths

#ouija_story_paths = find_ouija_stories(path0 = '/Users/lasse/Desktop/my/youtube', search="2025-07-02")

# ouija_story_paths = find_ouija_stories(path0 = '/Users/lasse/Desktop/my/youtube')

