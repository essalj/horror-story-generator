import tools_query_openrouter as tqo
import tools_file_operations as tfo



def generate_youtube_description(genre, title, bookmarks, model="gpt-4"):
    """
    Generates a YouTube video description using AI.
    """
    prompt = tfo.open_file('prompt_library/yt_desc_ouija_stories.md')

def generate_youtube_description(genre, title, bookmarks, model="gpt-4"):
    """
    Generates a YouTube video description using AI.
    """

    if "ouija" in genre.lower() or "ouija" in title.lower():
        prompt = tfo.open_file('prompt_library/yt_desc_ouija_stories.md')
    else:
        value = 2
    prompt = f"""
You are an expert YouTube content creator and SEO specialist. Your task is to generate a highly engaging and SEO-optimized YouTube video description for a horror story compilation.

Here's the information you need:
- Video Title: "{title}"
- Story Genre: "{genre}"
- Video Bookmarks/Timestamps: {bookmarks}

The description should:
1.  Start with the video title.
2.  Include a compelling introduction that hooks viewers and integrates keywords like "scary stories", "horror compilation", "sleep aid", "rain sounds", "true stories", "ouija board", "paranormal", "creepy tales".
3.  Clearly list the bookmarks/timestamps.
4.  Include relevant hashtags.
5.  Have a strong call to action for liking, subscribing, and commenting.
6.  Mention the channel's membership link.
7.  Explain why horror stories can help with sleep (the provided text below).
8.  Be optimized for YouTube search and ranking.

Here's the text explaining why horror stories help with sleep:
"Why do horror stories help you sleep?
Horror stories trigger physiological fear responses, which in turn reduces cortisol levels. They are a kind of “mental training” or “exposure therapy” for people with various forms of stress or anxiety. Fans of horror seek out these stories to destress, to regulate their emotions, and even to meditate and sleep."

Do NOT include any YouTube links in the generated description.
"""
    # The system_role is integrated into the prompt for query_openrouter
    generated_description = tqo.query_openrouter(prompt=prompt, model=model)
    return generated_description
    
#yt_description = generate_youtube_description(genre, title=genre, bookmarks = bookmarks)

def generate_community_post(genre, model="gpt-4"):
    """
    Generates a YouTube community post using AI.
    """
    prompt = f"""
You are an expert YouTube community manager. Your task is to create a short, engaging YouTube community post to announce a new video.

Here's the information you need:
- Story Genre: "{genre}"

The post should:
1.  Be concise and attention-grabbing.
2.  Mention the new video is a compilation of true scary {genre} stories with rain sounds.
3.  Encourage viewers to watch.
4.  Include relevant hashtags.
5.  Use emojis.

Do NOT include any YouTube links in the generated post.
"""
    # The system_role is integrated into the prompt for query_openrouter
    generated_post = tqo.query_openrouter(prompt=prompt, model=model)
    return generated_post

def generate_reminder_post(genre, model="gpt-4"):
    """
    Generates a reminder post for social media using AI.
    """
    prompt = f"""
You are an expert social media manager. Your task is to create a short, engaging reminder post for social media (e.g., Twitter, Instagram story) about a recently released YouTube video.

Here's the information you need:
- Story Genre: "{genre}"

The post should:
1.  Be concise and attention-grabbing.
2.  Remind followers about the "True Scary {genre} Stories For Sleep With Rain Sounds" video.
3.  Encourage them to watch if they missed it.
4.  Include relevant hashtags.
5.  Use emojis.

Do NOT include any YouTube links in the generated post.
"""
    # The system_role is integrated into the prompt for query_openrouter
    generated_reminder = tqo.query_openrouter(prompt=prompt, model=model)
    return generated_reminder


import os
def save_generated_content(xp_path, yt_description, community_post_1, community_post_2):
    """
    Saves the generated YouTube description and community posts to text files
    in the specified output folder.
    """
    yt_desc_filepath = os.path.join(xp_path, "youtube_description.txt")
    community_post_1_filepath = os.path.join(xp_path, "community_post_1.txt")
    community_post_2_filepath = os.path.join(xp_path, "community_post_2.txt")

    with open(yt_desc_filepath, "w", encoding="utf-8") as f:
        f.write(yt_description)
    print(f"YouTube description saved to: {yt_desc_filepath}")

    with open(community_post_1_filepath, "w", encoding="utf-8") as f:
        f.write(community_post_1)
    print(f"Community post 1 saved to: {community_post_1_filepath}")

    with open(community_post_2_filepath, "w", encoding="utf-8") as f:
        f.write(community_post_2)
    print(f"Community post 2 saved to: {community_post_2_filepath}")

def main():
    # Example Usage
    genre = "Ouija Board"
    title_compilation = "True Scary Ouija Board Stories For Sleep With Rain Sounds | True Horror Stories | Fall Asleep Quick"
    bookmarks = "00:00:00 1. 00:01:24 2. 00:13:56 3. 00:24:17 4. 00:38:47 5. 00:49:58 6. 01:01:47"

    # Generate YouTube Description
    yt_description = generate_youtube_description(genre, title_compilation, bookmarks)
    print("--- YouTube Description ---")
    print(yt_description)
    print("\n" + "-"*30 + "\n")

    # Generate Community Post 1
    community_post_1 = generate_community_post(genre)
    print("--- Community Post 1 ---")
    print(community_post_1)
    print("\n" + "-"*30 + "\n")

    # Generate Community Post 2 (using reminder post for now, can be changed later)
    community_post_2 = generate_reminder_post(genre)
    print("--- Community Post 2 ---")
    print(community_post_2)
    print("\n" + "-"*30 + "\n")

    # For demonstration, let's assume a dummy xp_path for saving
    # In a real scenario, xp_path would be passed from the main flow
    dummy_xp_path = "/Users/lasse/Desktop/my/youtube/temp_generated_content"
    if not os.path.exists(dummy_xp_path):
        os.makedirs(dummy_xp_path)
    
    save_generated_content(dummy_xp_path, yt_description, community_post_1, community_post_2)

if __name__ == "__main__":
    main()