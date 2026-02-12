from flask import Flask, request, jsonify
import tools_mp4_creation_from_inputs as mp4_story_gen
import os

app = Flask(__name__)

@app.route('/create_mp4_story', methods=['POST'])
def create_mp4_story():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    story = data.get('story')
    image_prompts = data.get('image_prompts')
    gender = data.get('gender')
    title = data.get('title', 'generated_story') # Optional title for the output file

    if not all([story, image_prompts, gender]):
        return jsonify({"error": "Missing required parameters: 'story', 'image_prompts', and 'gender' are required."}), 400

    try:
        output_mp4_path = mp4_story_gen.create_mp4_from_inputs(story, image_prompts, gender, title)
        if output_mp4_path:
            return jsonify({"message": "MP4 story created successfully", "mp4_path": output_mp4_path}), 200
        else:
            return jsonify({"error": "Failed to create MP4 story"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # To run this service:
    # 1. Make sure you have Flask installed: pip install Flask
    # 2. Run this script: python mp4_story_service.py
    # 3. The service will be available at http://127.0.0.1:5000/create_mp4_story
    #    You can send POST requests with JSON payload:
    #    {
    #        "story": "Once upon a time...",
    #        "image_prompts": ["A dark forest", "A scary monster"],
    #        "gender": "female",
    #        "title": "MyCustomStory"
    #    }
    app.run(debug=True)
