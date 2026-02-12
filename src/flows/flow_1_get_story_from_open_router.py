import os
from time import time, sleep
import datetime
import tools_query_openrouter as tqo
import tools_file_operations as tfo
import tools_json_cleaner as tjc
import tools_json_extract_story_and_img as tj
import json
import re

# q1 ='''Use the master prompt below ("Master prompt for LLM Horror Story Generation Recipe
# ") to write a story based on this user input: I want a 1200 word sherif or cop story of a very scary case or shift. NO supernatural stuff
# '''
def get_story_and_prompts(q1: str, model = "google/gemini-2.5-flash"):
    """
    Gets a horror story and associated image prompts and gender from OpenRouter.

    Args:
        q1: The initial query string for the story generation.
        story_type: The type of story being generated (used for file naming).

    Returns:
        A tuple containing:
        - story (str or None): The generated horror story.
        - image_prompts (list of str): A list of image prompts.
        - gender (str or None): The gender of the main character.
    """
    # q1 = user_story_query

    master_prompt_path = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/prompt_library/opus46_2_scary story_master_prompt.md'
    master_prompt = tfo.open_file(master_prompt_path)
#    master_prompt = tfo.open_file('/Users/lasse/Desktop/my/Git/horror_story_trimmed/prompt_library/Master prompt for LLM Horror Story Generation Recipe.md')
    if len(q1)<5:
        q1 = "I want a scary ouija board story"
    q2 = 'Use the master prompt below ("Master prompt for LLM Horror Story Generation") to write a story based on this user input: ' + str(q1)
    q1x = q2 + "\n" + str(master_prompt)
    print(q1x)
    # r_json_response = tqo.query_openrouter(q1x, model=writer_model)
    
    r_json_response = tqo.query_openrouter_json(q1x, model=writer_model)
    # r_json_response = tfo.open_file('/Users/lasse/Desktop/my/Git/horror_story_trimmed/json_files/2026-02-09_163200-Trail story_extracted.json')
    # r_json_response = r

    datetime_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    # fnj = datetime_string + " - json_response.json"
    fnj = "current_json_response.json"
    file_path_json = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/json_files/' + fnj
    tfo.save_file(file_path_json, str(r_json_response))




    story_title = None
    story = None
    image_prompts = []
    gender = None
    file_path = None

    # q_story_type = "u r a prof fiction writer. Figure out what story type the user is asking for. It can be 'ouija story', 'trucker story', 'sheriff story', 'cop story' ... or any type u think, but no more than 2 words. I want nothing but the story type as output - NO MORE THAN 2 WORDS. This is the user input: " +str(q1)
    story_type = genre

    # writer_model = 'anthropic/claude-opus-4.6'

    #t_content_string = json.loads(r_json_response)['choices'][0]['message']['content']


    # json_str = r_json_response
    # json_prompt ='/Users/lasse/Desktop/my/Git/horror_story_trimmed/prompt_library/agent_json_fixer.md'
    # json_fix_prompt = tfo.open_file(json_prompt) + str(json_str) 
    # fixed_json = json.loads(tqo.query_openrouter(prompt=json_fix_prompt, model=writer_model))
    # content_string = fixed_json['choices'][0]['message']['content']
    # content_string = r_json_response['choices'][0]['message']['content']

    # Extract the content string from the nested structure
    try:
        content_string = r_json_response['choices'][0]['message']['content']

        # Assuming the structure is r_json_response['choices'][0]['message']['content']
        # content_string = json.loads(r_json_response)['choices'][0]['message']['content']

        # # Clean the markdown code fences
        # if content_string.startswith("```json"):
        #     content_string = content_string[len("```json"):].strip()
        # if content_string.endswith("```"):
        #     content_string = content_string[:-len("```")].strip()

        # Remove invalid control characters from the content string
        # Remove invalid characters that are not printable ASCII or common JSON escapes
        # This regex keeps printable ASCII characters (32-126) and allows for escaped backslashes and quotes
        # It also explicitly allows \n, \r, and \t which are valid in JSON strings when escaped
        # This is a more aggressive cleaning to handle potential hidden invalid characters
        # cleaned_content_string = re.sub(r'[^\x20-\x7E\\]', '', content_string)
        # Further refine to handle escaped quotes and backslashes correctly if needed,
        # but the primary issue is likely unescaped control characters.
        # Let's try this first.
        # content_string = cleaned_content_string

        # # Find the index of the last closing brace and truncate the string there
        # last_brace_index = content_string.rfind('}')
        # if last_brace_index != -1:
        #     content_string = content_string[:last_brace_index + 1]
        # else:
        #     # Handle the case where no closing brace is found (shouldn't happen with valid JSON)
        #     print("Warning: No closing brace found in JSON string.")


        # Save the cleaned JSON string to a file (optional, for debugging)
        datetime_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        fn = datetime_string + "-" + story_type + ".json"
        file_path = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/json_files/' + fn
        tfo.save_file(file_path, content_string)

        print(f"Saved raw LLM response (after markdown cleaning) to: {file_path}")


        # --- New Approach: Use another LLM call to extract data ---
        extraction_prompt = """Extract the following information from the text below:
        - The story, which is tagged with "story". Output this as a single string.
        - The image prompts, which are in a list tagged with "image_prompts". Output these as a list of strings (just the prompt descriptions).
        - The gender of the storyteller, which is tagged with "storyteller_gender". Output this as a string.

        Provide the extracted information and NOTHING MORE as a JSON object with the keys "extracted_story", "extracted_image_prompts", and "extracted_gender". 
        DO NOT include any other text or markdown code fences. The first character of your response must be '{' and the last character must be '}'.
        IF YOU OUTPUT ANYTHING ELSE THAN THEH REQUESTED THEN IT WILL BE CONSIDERED A FAILURE!!!
        --------------
        Text to extract from:
        """ + content_string

        # Query OpenRouter again for extraction
        extraction_response = tqo.query_openrouter(extraction_prompt, model=worker_model)

        # The extraction_response should be a parsed JSON object (dict)
        # It should have keys "extracted_story", "extracted_image_prompts", "extracted_gender"
        #  story_type ="horror"
        # Save the extraction response to a file for inspection
        # extraction_fn = datetime_string + "-" + story_type + "_extracted.json"
        # extraction_file_path = '/Users/lasse/Desktop/my/Git/horror_story_trimmed/json_files/' + extraction_fn
        # tfo.save_file(extraction_file_path, json.dumps(extraction_response, indent=2)) # Save as formatted JSON string

        # print(f"Saved LLM extraction response to: {extraction_file_path}")


        # # Extract the content string from the nested structure of the extraction response
        try:
        #     # Assuming the structure is extraction_response['choices'][0]['message']['content']
        #     extracted_content_string = extraction_response['choices'][0]['message']['content']

        #     # Clean the markdown code fences from the extracted content string
        #     if extracted_content_string.startswith("```json"):
        #         extracted_content_string = extracted_content_string[len("```json"):].strip()
        #     if extracted_content_string.endswith("```"):
        #         extracted_content_string = extracted_content_string[:-len("```")].strip()


            # Parse the extracted content string as a JSON object
            extracted_data = json.loads(extracted_content_string)

            # Extract story, image prompts, and gender from the extracted data
            story = extracted_data.get("extracted_story")
            image_prompts = extracted_data.get("extracted_image_prompts", []) # Default to empty list if key is missing
            gender = extracted_data.get("extracted_gender")
            if len(gender)<2 or gender is None:
                gender = "Male"

            # Add print statements to inspect extracted values
            print("\n--- Extracted Values (from second LLM call) ---")
            print(f"Story is None: {story is None}")
            print(f"Image Prompts is empty: {not image_prompts}")
            print(f"Gender is None: {gender is None}")

        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"\nAn error occurred while processing the extraction LLM response: {e}")
            story = None
            image_prompts = []
            gender = None

        # Check for successful extraction of story and gender
        if story is not None and gender is not None:
            print("\nSuccessfully extracted story and gender using LLM extraction.")
            print("--- Story ---")
            # Print first 500 chars of story, handling potential None or short story
            print((story[:500] + "...") if story and len(story) > 500 else story)
            print("\n--- Gender ---")
            print(gender)
            q2x = "Create a good short title for this story. Return nothing but the title and use only letters: " + story
            story_title = tqo.query_openrouter(q2x, model=model)

            # Check if image prompts were extracted
            if image_prompts:
                print("\n--- Image Prompts ---")
                # Print each image prompt on a new line for readability
                for i, prompt in enumerate(image_prompts):
                    print(f"Prompt {i+1}: {prompt}")
            else:
                print("\nNo image prompts were provided by the extraction LLM.")

        else:
            print("\nFailed to extract story or gender using LLM extraction.")
            # Handle the failure case

    except Exception as e:
        print(f"\nAn error occurred during the LLM extraction process: {e}")
        # Handle the exception

    # return story, image_prompts, gender, file_path, story_title
    return story, image_prompts, gender, story_title


def no_run():
# Example usage (optional - can be removed if this script is only imported)
#if __name__ == "__main__":
   # print("main")
    # Define example inputs
    example_q1 = '''Using the master prompt below ("Master prompt for LLM Horror Story Generation Recipe"), write a story based on this user input: "I want a 1200 word sherif or cop story of a very scary case or shift. NO supernatural stuff".
            Your response MUST be a raw JSON object with the following top-level keys:
            - "story": The generated horror story (string).
            - "image_prompts": A list of strings, where each string is a detailed prompt for generating an image related to the story.
            - "gender": The gender of the main character in the story (string, e.g., "Male", "Female", "Non-binary").

            DO NOT include any extra text, explanations, or markdown code fences (```json). The first character of your response must be '{' and the last character must be '}'.
            '''
    example_story_type = "cop_stories"

    # Call the function
    generated_story, generated_image_prompts, generated_gender = get_story_and_prompts(example_q1, example_story_type)

    # Print the results
    print("\n--- Function Output ---")
    print(f"Generated Story (first 100 chars): {(generated_story[:100] + '...') if generated_story and len(generated_story) > 100 else generated_story}")
    print(f"Generated Image Prompts count: {len(generated_image_prompts)}")
    print(f"Generated Gender: {generated_gender}")
    


    