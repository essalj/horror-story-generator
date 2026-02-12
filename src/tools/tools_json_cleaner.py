import json

def clean_json_markdown(raw_text):
    """
    Removes markdown code fences ('```json' and '```') from a string
    if they are present.

    Args:
        raw_text (str): The input string, potentially containing JSON
                        wrapped in markdown fences.

    Returns:
        str: The cleaned string with markdown fences removed, or the
             original string if fences were not found.
    """
    cleaned_text = raw_text.strip() # Remove leading/trailing whitespace

    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[len("```json"):].lstrip() # Remove prefix and leading whitespace

    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-len("```")].rstrip() # Remove suffix and trailing whitespace

    return cleaned_text

if __name__ == '__main__':
    # Example Usage:
    markdown_json = """```json
{
  "name": "Test",
  "value": 123
}
```"""

    clean_json = clean_json_markdown(markdown_json)
    print("Cleaned JSON:")
    print(clean_json)

    try:
        json_object = json.loads(clean_json)
        print("\nSuccessfully parsed cleaned JSON:")
        print(json_object)
    except json.JSONDecodeError as e:
        print(f"\nError decoding cleaned JSON: {e}")

    plain_json = """{
  "name": "Plain",
  "value": 456
}"""
    clean_plain = clean_json_markdown(plain_json)
    print("\nCleaned Plain JSON:")
    print(clean_plain)

    try:
        json_object_plain = json.loads(clean_plain)
        print("\nSuccessfully parsed cleaned Plain JSON:")
        print(json_object_plain)
    except json.JSONDecodeError as e:
        print(f"\nError decoding cleaned Plain JSON: {e}")