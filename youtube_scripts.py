import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# --- Configuration ---
# Replace with your YouTube Data API credentials
# You can obtain these from the Google Cloud Console:
# https://console.cloud.google.com/apis/credentials
CLIENT_SECRETS_FILE = "client_secrets.json" # You'll need to create this file
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"



def get_authenticated_service():
    """Authenticates and returns a YouTube API service object."""
    credentials = None

    # Check if a previously authorized token exists
    if os.path.exists("token.json"):
        with open("token.json", "r") as token_file:
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(token_file, SCOPES)

    # If there are no valid credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token_file:
            token_file.write(credentials.to_json())

    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, file_path, title, description, tags, category_id="24", privacy_status="private"):
    """Uploads a video to YouTube."""
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    try:
        # Call the API's videos.insert method to create and upload the video.
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
        )
        response = request.execute()
        print(f"Video uploaded successfully! Video ID: {response['id']}")
        return response
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None

def get_video_details(youtube, video_id):
    """Retrieves details of a specific YouTube video."""
    try:
        request = youtube.videos().list(
            part="snippet,status",
            id=video_id
        )
        response = request.execute()
        if response.get("items"):
            return response["items"][0]
        else:
            print(f"No video found with ID: {video_id}")
            return None
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None

def update_video_details(youtube, video_id, title=None, description=None, tags=None, category_id=None, privacy_status=None):
    """Updates details of a specific YouTube video."""
    video_update_body = {}
    snippet_update = {}
    status_update = {}

    if title:
        snippet_update["title"] = title
    if description:
        snippet_update["description"] = description
    if tags is not None: # tags can be an empty list
        snippet_update["tags"] = tags
    if category_id:
        snippet_update["categoryId"] = category_id
    if privacy_status:
        status_update["privacyStatus"] = privacy_status

    if snippet_update:
        video_update_body["snippet"] = snippet_update
    if status_update:
        video_update_body["status"] = status_update

    if not video_update_body:
        print("No details provided to update.")
        return None

    try:
        request = youtube.videos().update(
            part="snippet,status",
            body={
                "id": video_id,
                **video_update_body
            }
        )
        response = request.execute()
        print(f"Video details updated successfully for Video ID: {video_id}")
        return response
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None

if __name__ == "__main__":
    # --- Example Usage ---
    # You will need to:
    # 1. Create a client_secrets.json file with your OAuth 2.0 client ID and secret.
    #    Example:
    #    {
    #      "installed": {
    #        "client_id": "YOUR_CLIENT_ID",
    #        "project_id": "YOUR_PROJECT_ID",
    #        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #        "token_uri": "https://oauth2.googleapis.com/token",
    #        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #        "client_secret": "YOUR_CLIENT_SECRET",
    #        "redirect_uris": ["http://localhost"]
    #      }
    #    }
    # 2. Replace placeholders below with your actual video file path and desired properties.
    # 3. Ensure you have a video file to upload.

    # --- Step 1: Get YouTube Service ---
    youtube_service = get_authenticated_service()

    # --- Step 2: Upload a video ---
    video_file_to_upload = '/Users/lasse/Desktop/my/youtube/2025-08-06_2201_Disturbing True Ouija Horror Stories_compilation/scary-ouija-board-games-gone-wrong.mp4' # <-- CHANGE THIS
    new_video_title = "9 True Scary Ouija Board Game Gone WRONG Stories | RAIN SOUNDS"
    new_video_description = "This is a description for my awesome video."
    new_video_tags = ["Ouija Board Stories", "Horror Stories", "Sleep Stories"]
    new_video_category_id = "24" # Example: Education
    new_video_privacy_status = "public" # Options: "public", "private", "unlisted"

    if os.path.exists(video_file_to_upload):
        print("Q")
        uploaded_video_info = upload_video(
            youtube_service,
            video_file_to_upload,
            new_video_title,
            new_video_description,
            new_video_tags,
            new_video_category_id,
            new_video_privacy_status
        )

        if uploaded_video_info:
            uploaded_video_id = uploaded_video_info.get("id")

            # --- Step 3: Get details from an existing video ---
            # Replace 'EXISTING_VIDEO_ID' with the ID of a video you've already uploaded
            existing_video_id = 'VtY0hxvQomU' # <-- CHANGE THIS
            existing_video_details = get_video_details(youtube_service, existing_video_id)

            if existing_video_details:
                # Extract properties to copy
                title_to_copy = existing_video_details["snippet"].get("title")
                description_to_copy = existing_video_details["snippet"].get("description")
                tags_to_copy = existing_video_details["snippet"].get("tags")
                category_id_to_copy = existing_video_details["snippet"].get("categoryId")
                privacy_status_to_copy = existing_video_details["status"].get("privacyStatus")

                print("\n--- Details from existing video ---")
                print(f"Title: {title_to_copy}")
                print(f"Description: {description_to_copy}")
                print(f"Tags: {tags_to_copy}")
                print(f"Category ID: {category_id_to_copy}")
                print(f"Privacy Status: {privacy_status_to_copy}")
                print("----------------------------------\n")

                # --- Step 4: Update the newly uploaded video with copied properties ---
                update_video_details(
                    youtube_service,
                    uploaded_video_id,
                    title=title_to_copy,
                    description=description_to_copy,
                    tags=tags_to_copy,
                    category_id=category_id_to_copy,
                    privacy_status=privacy_status_to_copy
                )
            else:
                print("Could not retrieve details from the existing video. Skipping update.")
    else:
        print(f"Error: Video file not found at {video_file_to_upload}")
