
import requests
import os
import json


from dotenv import load_dotenv
load_dotenv()  # Loads into os.environ
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Optional: assign to variable
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env")
else:
    print(f"OPENROUTER_API_KEY loaded successfully: {OPENROUTER_API_KEY}")


# Replace with your actual OpenRouter API key or use an environment variable
# It's recommended to use environment variables for security
# OPENROUTER_API_KEY = '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'
# writer_model = 'moonshotai/kimi-k2.5'


def query_openrouter(prompt, model="google/gemini-2.5-flash"):
    """
    Sends a query to the OpenRouter API and returns the response.

    Args:
        prompt (str): The prompt to send to the model.
        model (str): The model to use for the query (default: mistralai/mistral-7b-instruct:free).

    Returns:
        str: The model's response, or an error message if the request failed.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error querying OpenRouter: {e}"

def get_openrouter_models():
    """
    Gets the list of available model names from the OpenRouter API.

    Returns:
        list: A list of model names, or an error message if the request failed.
    """
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        models_data = response.json().get("data", [])
        model_names = [model.get("id") for model in models_data if model.get("id")]
        return model_names
    except requests.exceptions.RequestException as e:
        return f"Error getting OpenRouter models: {e}"

get_openrouter_models()

#prompt = q1x
def query_openrouter_json(prompt, model="google/gemini-2.5-flash"):
    # "mistralai/mistral-7b-instruct:free")
    print("----------------------")
    print("##### model used in qery_openrouter_json:  " + model)
    print("----------------------")

    """
    Sends a query to the OpenRouter API and returns the full JSON response.

    Args:
        prompt (str): The prompt to send to the model.
        model (str): The model to use for the query (default: mistralai/mistral-7b-instruct:free).

    Returns:
        dict: The full JSON response from the API, or None if the request failed.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    print("test print query_openrouter_json : after data")

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        r = response.json()
        return r
    except requests.exceptions.RequestException as e:
        print(f"Error querying OpenRouter: {e}")
        return None
    # qt ="hvadd er 2*3"
    # query_openrouter_json(prompt, model=writer_model)
    
#examples


    # Example usage for querying a model:
    user_query = "Write a short horror story about a haunted house on 100 words."
    response_text = query_openrouter(user_query, model=writer_model)
    # response_text = query_openrouter(user_query, model="google/gemini-2.5-flash")
    print("\nQuery Response:")
    print(response_text)


# Example usage for querying a model and getting JSON response:

    user_query = "Write a short horror story about a haunted house on 100 words."
    json_response = query_openrouter_json(user_query, model=writer_model)
    # json_response = query_openrouter_json(user_query, model="google/gemini-2.5-flash")
    print("\nQuery JSON Response:")
    print(json_response)

