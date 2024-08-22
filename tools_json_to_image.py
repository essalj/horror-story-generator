import json
import os
import tools_create_images as tci
    

# Example usage
# json_input = '''
# [
#     {"prompt": "A serene lake at sunset"},
#     {"prompt": "A futuristic cityscape"},
#     {"prompt": "A whimsical forest with magical creatures"}
# ]
# '''


def image_prompts_from_json(fn_json):
    with open(fn_json, 'r', encoding='utf-8') as file:
        stories = json.load(file)

    if stories:
        print(f"Found {len(stories)} stories:")
        for i, story in enumerate(stories, 1):
            print(f"Story {i}:")
            if 'summary' in story:
                print(f"  Summary: {story['summary'][:100]}...")  # Print first 100 characters of the summary
            if 'characters' in story:
                print(f"  Number of characters: {len(story['characters'])}")
            if 'scenes' in story:
                print(f"  Number of scenes: {len(story['scenes'])}")
                for j, scene in enumerate(story['scenes'], 1):
                    print(f"    Scene {j}: {scene['heading']}")
                    print(f"      Image Prompt: {scene['imagePrompt'][:50]}...")  # Print first 50 characters of the prompt
    else:
        print("No stories were loaded.")

    try:
        scenes = []
        image_prompts = []
        for story in stories:
            if 'scenes' in story:
                scenes.extend(story['scenes'])

        for i, scene in enumerate(scenes):
            image_prompt = "Title: " + scene['heading'] + "\n" + scene['imagePrompt']
            image_prompts.append(image_prompt)
            print(image_prompt + "\n------------------------\n")
    except:
        image_prompts =["No images"]
    
    return image_prompts


# def create_images_from_json(fn_json, xp_path):
#     image_prompts = image_prompts_from_json(fn_json=fn_json)

#     image_files = []    
#     for i, img_prompt in enumerate(image_prompts):
#         # print(img_prompt)
#         fn = "image_" + str(100+i)
#         # print(fn)
#         try:
#             path_img = os.path.join(xp_path, fn + " - img")
#             print(path_img)
#             image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn= path_img, i=10 + i)
#             image_files.append(filename)
#         except:
#             print("failed image " + str(100+i))

#     return image_files

def create_images_from_json(fn_json, xp_path):
    image_prompts = image_prompts_from_json(fn_json=fn_json)

    image_files = []    
    for i, img_prompt in enumerate(image_prompts):
        fn = "image_" + str(100+i)
        path_img = os.path.join(xp_path, fn + " - img")
        print(path_img)

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                image_url, filename = tci.chatgpt_dalle(prompt=img_prompt, fn=path_img, i=10 + i)
                image_files.append(filename)
                break  # If successful, exit the loop
            except Exception as e:
                if attempt == max_attempts - 1:  # If it's the last attempt
                    print(f"Failed to create image {100+i} after {max_attempts} attempts. Error: {str(e)}")
                else:
                    print(f"Attempt {attempt + 1} failed for image {100+i}. Retrying...")

    return image_files


# usage
# xp_path = r"C:\my\__youtube\videos\Horror_stories_test\story_1_test"  # Replace with your desired path
# fn_json = r"C:\my\__youtube\videos\Horror_stories_test\story_1_test\horror-story-analysis.json"

# fn_json = r"C:\my\__youtube\videos\2024-08-19_1102_Truly Scary Shifting Reality and Parallel Universe Stories - v2\glitch-in-the-matrix-analysis.json"
# xp_path = r"C:\my\__youtube\videos\2024-08-19_1102_Truly Scary Shifting Reality and Parallel Universe Stories - v2"

# image_files = create_images_from_json(fn_json, xp_path)


