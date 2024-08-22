I apologize for the confusion. You're right, I should have included the full task description. Here's the complete task, including all steps before the JSON structure:

# Story Analysis, Character Profiling, and Scene Visualization Task

## 1. Read the Story
Carefully read the provided text-based story.

## 2. Create a Summary
Write a concise summary of the story (1-2 paragraphs).

## 3. Develop Character Profiles
Create detailed visual descriptions for the main characters:

CRITICAL INSTRUCTION: For ALL character profiles, you MUST provide specific, concrete details for EVERY single characteristic and physical trait listed below. DO NOT use vague terms like "unspecified" or leave any field blank. If a detail isn't explicitly mentioned in the story, YOU HAVE TO use imagination to create a fitting attribute that aligns with the character and narrative. Be thorough and imaginative – every aspect of the character should be clearly defined. Ensure all details, whether from the original text or created, are consistent with the story and presented as definitive aspects of the character.
!!It is utmost important that race, gender, age and skin color is alwayls filled with a valid value!!

### a. Protagonist Profile
- Name and gender
- Race and skin color
- Age
- Height and body type
- Hair color and style
- Eye color
- Facial features (including nose, mouth, etc.)
- Distinctive features
- Typical attire or clothing style
- Key personality traits
- Relevant skills
- Brief backstory related to their role in the narrative

### b. Supporting Character Profiles (up to 2)
- Follow the same structure as the protagonist profile
- Ensure distinct appearances, attire, and personalities
- Explain how they complement the protagonist and contribute to the story

**Note:** 
Remember: The goal is to paint a vivid, comprehensive picture of each character. Your descriptions should enable anyone to visualize the character clearly and understand their role in the story.

## 4. Scene Visualization
Split the story into distinct scenes. For each scene:

### a. Scene Heading
Provide a brief, descriptive heading for the scene.

### b. Image Prompt
Create a detailed image prompt for a key moment in the scene:

- Use your talents as a digital artist to visualize the scene with the protagonist always as the primary focus.
- **CRITICAL: For EVERY image prompt, you MUST list ALL physical characteristics in parentheses for EACH character EVERY time they appear, regardless of whether they've been described before.** There should be no use of phrases like "as described earlier" or any shortcuts in character descriptions.
- This comprehensive list MUST include for each character appearance: name, race, skin color, age, height, body type, hair color and style, eye color, facial features, distinctive features, and typical attire. For example: "Sarah (Caucasian, fair skin, 28 years old, 5'6", athletic build, long wavy blonde hair, bright green eyes, small nose, full lips, freckles across her cheeks, wearing casual sportswear)".
- Repeat this full description for every character in every scene, even if they've appeared before. This ensures absolute consistency and allows for accurate visualization in each individual prompt.
- Describe the protagonist and up to two supporting characters involved in the scene, ensuring detailed character consistency by meticulously referencing the generated Character profiles.
- Include setting details (time of day, location), important objects, and environmental elements to convey the mood or atmosphere.
- Ensure that the style of the image is consistent across all scenes. Make the images photo-realistic, as if captured by a Hasselblad camera.
- Ensure the protagonist's prominence in the scene, with supporting characters positioned to highlight their relationship and interactions with the protagonist.
- Make sure the prompt complies with OpenAI's policy for image generation. Do not mention any brands.

Remember: Repeating full character descriptions in every scene is crucial for maintaining consistency and providing clear, standalone image prompts. This approach ensures that each prompt contains all necessary information without relying on previous descriptions.


## 5. Organize Output in JSON Format
After completing the story analysis, character profiling, and scene visualization, organize all the information into a JSON structure following this template:

```
[
{
  "summary": "",
  "characters": [
    {
      "role": "Protagonist",
      "name": "",
      "gender": "",
      "race": "",
      "skin color": "",
      "age": "",
      "height": "",
      "bodyType": "",
      "hair": {
        "color": "",
        "style": ""
      },
      "eyeColor": "",
      "facialFeatures": "",
      "distinctiveFeatures": "",
      "typicalAttire": "",
      "personalityTraits": [],
      "skills": [],
      "backstory": ""
    },
    {
      "role": "Supporting Character 1",
      "name": "",
      "gender": "",
      "race": "",
      "skin color": "",
      "age": "",
      "height": "",
      "bodyType": "",
      "hair": {
        "color": "",
        "style": ""
      },
      "eyeColor": "",
      "facialFeatures": "",
      "distinctiveFeatures": "",
      "typicalAttire": "",
      "personalityTraits": [],
      "skills": [],
      "backstory": "",
      "relationToProtagonist": ""
    },
    {
      "role": "Supporting Character 2",
      "name": "",
      "gender": "",
      "race": "",
      "skin color": "",
      "age": "",
      "height": "",
      "bodyType": "",
      "hair": {
        "color": "",
        "style": ""
      },
      "eyeColor": "",
      "facialFeatures": "",
      "distinctiveFeatures": "",
      "typicalAttire": "",
      "personalityTraits": [],
      "skills": [],
      "backstory": "",
      "relationToProtagonist": ""
    }
  ],
  "scenes": [
    {
      "heading": "",
      "imagePrompt": ""
    }
  ]
}
]
```

When filling out this JSON structure:

1. Ensure the summary is concise but covers the main plot points.
2. Fill out all character details completely, using the information from the character profiles created in step 3.
3. Include ALL scenes from the story, each with a clear heading and a detailed image prompt.
4. Each image prompt should incorporate all relevant character descriptions and setting details.
5. Make sure the JSON structure is properly formatted and valid.

The task output should consist solely of this JSON object.