
#pip install Pillow
# pip install pydub


import re
import os
import openai
from openai import OpenAI
from time import time,sleep
import datetime


# story_type = "home_alone"
# genre = "SCARY Home Alone Stories"
# user_input = ""
def story_generator(
        story_type = "Tinder",
        genre = "True Scary Tinder Dating Stories", 
        user_input = "A tinder date that goes horriblly wrong"):


    error_list = []
    
    ####################
    
    # Story settings
    ####################

    # select model
    # gpt4 = "gpt-4-turbo-preview"
    # gpt4 = "o3-mini-2025-01-31"
    # gpt4 = "gpt-4.5-preview"
    # gpt4 = "gpt-4-turbo"
    # gpt3 = "GPT-4o mini"
    #    o4_mini = "o3-mini" 
    gpt4 = "gpt-4.1"
    gpt4mini = "gpt-4.1-mini"
    #    selected_gpt = gpt41
    selected_gpt = gpt4mini


    narration_style = "Opt for a first-person narrative to deepen the story's immersive quality."
    # narration_style = "Choose what you think suits the story best."
    fn = "Stories"  #file name
    beats_split = ['7','1-2','3-5','6-7']  # count. part 1, 2, 3
    # beats_split = ['6','1-2','3-4','5-6']  # count. part 1, 2, 3
    count_action_beats = int(beats_split[0])


    no_of_pitches = 5 # to select the best story
    
    
    ############################



    def create_dated_folder(base_path, text_add_on):
        # Get today's date in yyyy-mm-dd format
        # today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        # datetime_string = now.strftime("%Y%m%d_%H%M")
        datetime_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        folder_name = f"{datetime_string}_{text_add_on}"

        # Create the full path for the new folder
        new_folder_path = os.path.join(base_path, folder_name)

        # Create the folder
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"Folder created: {new_folder_path}")
        else:
            print(f"Folder already exists: {new_folder_path}")
        return new_folder_path


    def open_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()
        

    def save_file(filepath, content):
        with open(filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(content)
            

    def count_words(my_string):
        words = re.findall(r'\b\w+\b', my_string)
        number_of_words = len(words)
        print("Number of words:", number_of_words)



    #############################
    ## Create folder for export
    #############################
    # Create folder
    cwd_path = os.getcwd()
    xp_path_0 = '/Users/lasse/Desktop/my/youtube/videos'  #mac #".."    
    # "C:\\my\\__youtube\\videos" pc

    #xp_path_0 = "C:\\my\\__youtube\\videos" #pc
    additional_text = genre  # Replace with your desired text
    xp_path = create_dated_folder(xp_path_0, additional_text)
    # print(xp_path)
    # xp_path = r"C:\my\__youtube\videos\2024-02-29_1337_True Walmart Horror Stories"

    ###################
    # Define chatbot
    ###################
    break_line = "\n" + 50*"-" + "\n"


    #openai_api_key = open_file('openaiapikey.txt') #pc
    openai_api_key = open_file('/Users/lasse/Desktop/my/Git/api-keys/openaiapikey.txt')

    client = OpenAI(api_key=openai_api_key)
    # system_role = open_file("chatbot_horror_writer_role.txt")
    system_role = open_file("prompt_library/Claude - horror-writing-expert-prompt.md")
    # task = open_file("assistant_horror_task.txt")
    sleep(5)



    #1. create assistant
    selected_gpt = "gpt-4" # Or another suitable model
    assistant = client.beta.assistants.create(
        # instructions="You are a helpful assistant and a master of creating short horror stories",
        instructions = system_role,
        # tools=[{"type": "code_interpreter"}],
        model = selected_gpt)

    print(assistant)
    print(assistant.id)   # asst_gmluHapfEinMNLGcSgvsbenO
    sleep(5)


    #2. create thread
    thread = client.beta.threads.create()
    print(thread)
    print(thread.id) # thread_RUAndXpEbqXiXrtKx2MC0Fu5
    thread_id = thread.id


    def new_msg(task):
        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user",
            # content="Can you write me 3 good titles for an Airbnb horror story?"
            content = task
        )
        
        #run Assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Help the user as best you can. Refrain from using the name Alex in the stories you write"
        )

        #Check the run status
        tt = 0
        while True:
            try:
                t0 = 5
                tt = tt + t0
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                print(f"Run status:{run.status} - " + str(tt) + " seconds.")
                if run.status=='completed':
                    break
                sleep(t0)
            except Exception as e:
                print(f"Error retrieving run status: {e}")
                sleep(t0) # Wait before retrying

        #Display messages when run completes
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value  # gets newest reponse from thread
        # print(response)
        return response
    # r = new_msg("What is the gender of the protagonist")
    # print(r)


    t1_camping = f'''
        Wilderness Horror Story Generation Task

        Objective: Create an intensely frightening camping/wilderness horror story.

        Story Foundation:
        -Central Theme: A terrifying encounter in an isolated outdoor setting. Explore the primal fears of being cut off from civilization, the overwhelming presence of wilderness, and the vulnerability of the human experience against nature or unknown threats.
        -Psychological and Survival Elements: Combine psychological terror with the harsh realities of survival. Characters face both external threats and their own deteriorating mental state as isolation and fear take hold.
        -First-Person Recollection: Narrate as a personal memory, mimicking the authentic accounts found in Reddit's true outdoor horror stories for maximum impact and believability.
        -Climax and Revelation: Include a revelation or twist that shatters the narrator's sense of safety, like discovering the true nature of a threat, realizing they're being stalked, or uncovering something that shouldn't exist in the wilderness.

        Inspiration & Story Ideas:
        1. The Hungry Pack: After a late-season snowstorm traps a group of campers, they realize a pack of wolves is circling their tent, growing bolder as hunger sets in and the group’s supplies dwindle.
        2. Grizzly Territory: A solo backpacker accidentally sets up camp near a grizzly’s den. As night falls, the bear returns, and the camper must survive until dawn with only a thin tent and their wits for protection.
        3. The Hermit’s Warning: Deep in the forest, campers encounter a reclusive hermit who warns them to leave before nightfall. Ignoring the warning, they soon realize they’re being stalked—not just by the hermit, but by something even he fears.
        4. The Fire Line: Campers wake to the smell of smoke and the distant roar of a wildfire. As they flee, they find themselves herded by unseen forces toward a part of the forest that doesn’t appear on any map.
        5. The Mimic in the Woods: Strange cries echo through the trees at night, perfectly imitating the voices of the campers’ loved ones. When one camper follows the sound, the group must decide whether to risk a rescue or barricade themselves and wait for daylight.
        6. The Vanishing Trail: A group of friends finds their trail markers replaced by strange symbols. As they try to find their way back, they realize they’re being watched by a mountain lion—and perhaps something even more sinister.
        7. The Lost Time Loop: Campers experience missing time and déjà vu, finding themselves trapped in a repeating night where the same terrifying events unfold, no matter what they do to change their fate.
        8. The Poisoned Grove: After foraging for wild berries, a camper falls violently ill and begins to hallucinate. The group must determine if it’s just the berries—or if something in the forest is using the illness to manipulate and separate them.
        9. The Abandoned Campsite: Hikers stumble upon a campsite that looks recently used, with food still warm on the fire, but no sign of its occupants. As they investigate, they find disturbing clues that suggest the campers were taken by something lurking in the woods.
        10. The Campfire Legend: The group tells a local urban legend around the fire, only to realize the details of the story are coming true—down to the mysterious footprints appearing around their tents and the chilling sense that they are being watched by something not quite human.

        Task Execution:
        Generate High-Concept Pitches:
        1. Write {no_of_pitches} high-concept pitches for a terrifying wilderness horror story that delves into {genre} themes.
            - Each pitch should feature a unique threat, compelling characters, high survival stakes, and an unforgettable conclusion.
            - These pitches should be particularly frightening, rooted in a first-person narrative as if someone is reliving a traumatic outdoor experience.
            - Base the pitches on {user_input} if provided.
            - **At least one pitch must be entirely original and not based on the provided inspiration ideas above.**

        2. Choose Your Narrative Lens:
            - Opt for a first-person narrative to enhance the story's immediacy and isolation.
            - Ensure the protagonist's survival instincts, fears, and decisions drive the story and intensify the danger.

        3. Develop the Story Pitch:
            - Craft a pitch that encapsulates the essence of a harrowing wilderness encounter, focusing on isolation and primal fear.
            - Ensure the pitch highlights the protagonist's vulnerability, the overwhelming nature of their surroundings, and the escalating threat.

        4. Inspiration Utilization:
            - Draw from the provided story ideas—combining elements or introducing your own wilderness horror twist.
            - The goal is to create a pitch that feels authentic, terrifying, and grounded in the realities of outdoor survival.
            - **Remember: At least one pitch must be completely original and not derived from the inspiration list.**

        5. Critique and Rate Pitches:
            - Assume the role of both a critic and an experienced outdoors person.
            - Evaluate the pitches on a scale from 1-100, prioritizing stories that masterfully blend survival horror with believable wilderness scenarios.
            - Pitches that lack authentic outdoor elements or realistic survival situations should receive lower ratings, while those that excel in creating genuine wilderness terror should score higher.

        6. Select the Best Pitch:
            - Choose the pitch with the highest rating based on its survival horror elements and how effectively it employs the isolation theme.
            - Consider the pitch's ability to evoke fear through wilderness settings, its survival authenticity, and its unique, terrifying twist.

        7. Output the Winning Pitch:
            - Present the selected pitch, its rating, and a detailed explanation for its top score.
            - Highlight how it stands out in terms of its realistic approach to wilderness horror, its survival elements, and its haunting impact on readers.
        '''




    t1_reddit_scary_stories = f'''
        Reddit-Style Scary Story Generation Task

        Objective: Create an intensely unsettling and psychologically terrifying story in the style of Reddit's popular scary stories. The story should feel authentic, as if recounted by someone who genuinely experienced the events.

        Story Foundation:
        - Realism: Ground the story in seemingly real-life situations that take a terrifying turn.
        - Narrative Perspective: First-person, mimicking a personal recollection or confession on a Reddit post.
        - Psychological Impact: Focus on the narrator's emotional and psychological state throughout the experience.
        - Pacing: Build tension gradually, with a powerful climax and a lingering sense of unease.
        - Ending: Craft a conclusion that leaves readers unsettled and questioning, as many real-life scary encounters often do.

        Key Elements to Incorporate:
        1. A compelling hook that immediately draws the reader in
        2. Vivid, sensory descriptions that make the experience feel real
        3. Subtle details that contribute to the overall sense of dread
        4. Exploration of common fears or relatable situations gone wrong
        5. Moments of escalating tension or near-misses
        6. A climactic scene that pushes the boundaries of what feels "real" while remaining plausible

        Inspirational Themes (Note: These are merely guidelines. Feel free to create your own unique concept):
        1. Stalker encounters
        2. Home invasions or unexplained occurrences at home
        3. Creepy interactions with strangers
        4. Unexplained phenomena
        5. Near-miss situations or narrow escapes
        6. Disturbing childhood memories
        7. Urban exploration gone wrong
        8. Workplace horror (especially during night shifts)
        9. Online dating horrors
        10. Camping or hiking incidents
        11. Paranormal experiences
        12. Creepy technology glitches

        Remember: While these themes are common in Reddit scary stories, they are only meant as inspiration. You are encouraged to develop your own unique idea that captures the essence of a real, terrifying experience.

        Task Execution:
        1. Develop a Unique Story Concept: Create an original story idea that feels like it could be a real experience shared on Reddit. While you can draw inspiration from the themes above, your story should be distinctly your own.

        2. Craft the Narrative Voice: Write in a first-person style that mimics the tone of someone sharing a true, personal story on Reddit. The voice should feel authentic and conversational.

        3. Build Tension and Realism: Focus on creating a sense of mounting dread through realistic details and plausible circumstances. The horror should come from the situation itself and the narrator's growing fear.

        4. Create Ambiguity: Leave some elements unexplained or open to interpretation, as many real-life scary encounters have unanswered questions.

        5. Evaluation Criteria: Judge your story based on its ability to feel like a genuine, terrifying experience, its psychological impact, and its lingering effect on the reader.

        Remember: The most effective Reddit-style scary stories often focus on the psychological impact of the experience rather than graphic details. The goal is to make the reader think, "This could happen to me," and leave them looking over their shoulder long after finishing the story.
        '''


    t1_occultism = f'''
    **Template for Occultism Horror Story Creation**

    **Task: Create a Short Horror Story for My YouTube Channel**

    **Pitch Requirements:**

    - **Rooted in Occult Realism:** The story should weave elements of the occult mystique into a narrative that feels plausible within its own universe, subtly blending supernatural with the everyday.
    - **Narrative Style:** The story must be told in the first person, giving the impression of a personal encounter with the occult. This approach should make the narrative feel as though it's being recounted from a deeply personal and unsettling memory.
    - **Unique Occult Twist:** Incorporate a distinctive twist related to the occult that sets this story apart from typical horror narratives. This twist should be original and enhance the eerie atmosphere.
    - **Complex Characters Involved with the Occult:** Develop characters that are multifaceted and drawn into the world of occultism through their interactions with occultism. These characters should drive the story, making their experiences compelling and relatable.
    - **High Emotional and Supernatural Stakes:** Craft a story with significant emotional depth, where the stakes are amplified by the supernatural elements at play. The outcome should deeply affect the reader, making the occult experience resonate on a personal level.


    **Task List:**

    1. **Generate High-Concept Pitches:** Write {no_of_pitches} high-concept pitches for a best-selling horror story that delves into  occult themes. Each pitch should feature a unique twist, engaging characters, high emotional stakes, and an unforgettable ending. These pitches should be particularly terrifying, rooted in a first-person narrative as if someone is reliving a haunting memory. Base the pitches on user input ("{user_input}") if provided.
    2. **Critique and Rate Pitches:** Assume the role of both a critic and an avid fan of short horror stories. Evaluate the pitches on a scale from 1-100, prioritizing stories that masterfully blend psychological terror with a touch of realism. Pitches that lack a believable foundation in the occult should receive lower ratings, while those that excel in psychological depth and terror should score higher.
    3. **Select the Best Pitch:** Choose the pitch with the highest rating based on its psychological terror, and how effectively it employs the occult and ouija board elements.
    4. **Output the Winning Pitch:** Present the selected pitch, its rating, and a detailed explanation for its top score. Highlight how it stands out in terms of its realistic approach to the occult, its emotional depth, and its unique, chilling twist.
    '''

    t1_tinder = f'''
    **Template for First-Person Tinder Dating Horror Narratives**

    **Objective: Develop a Short, Memorable Horror Story for My YouTube Channel**

    **Core Elements:**

    - **Authentic Digital Dating Dilemmas:** Weave a narrative that deeply explores the unsettling aspects of Tinder dating, rooted in genuine online interaction experiences. Stories should mirror plausible situations that take a horrifying turn, making listeners question the safety of their own digital dating ventures.

    - **Recollections of Horror:** Employ a first-person perspective to recount the tale as a vivid, unsettling memory. This approach should pull the audience into the narrative, as if they're hearing a distressing story from a trusted confidant, enhancing the personal connection and the story’s impact.

    - **Innovative Twist on Terror:** Center your story around a creative and shocking twist that morphs an ordinary Tinder encounter into a deeply disturbing event. This twist should be distinctive, adding a fresh layer of horror to the digital dating experience.

    - **Memorable Characters Through Memory:** Character development is key, with each persona richly painted through the protagonist's recollections. Their motivations, digital interactions, and eventual unraveling should be intricately detailed, contributing to the narrative’s suspense and horror.

    - **Emotional Depth and Resonance:** Construct your narrative to deeply resonate on an emotional level, with the protagonist's fears, desires, and nightmares at the forefront. The story should not only terrify but also evoke empathy, making the horror feel intensely personal and real.

    **Themes for Inspiration:**
    - Catfishing Nightmares: Encounters that unveil the shocking realities behind deceptively crafted online identities, leading to unexpected and sometimes dangerous discoveries.
    - Vanishing Acts: Tales of deep connections abruptly ending with one party disappearing without warning or explanation, leaving behind a haunting absence.
    - Stalker Shadows: Chilling accounts of relentless pursuit and harassment by a date, transforming initial attraction into a terrifying ordeal of fear and invasion.
    -Ex-Partner Encroachments: Horrific run-ins with dates' exes, whose unexpected interventions range from awkward disruptions to threatening confrontations.
    - Perilous Meetings: Stories of dates turning dangerous, where seemingly charming encounters escalate into life-threatening situations requiring quick escapes.
    - Manipulative Motives: Experiences of being exploited for money, information, or other sinister aims, masked under the pretense of romantic interest.
    - Creepy Companions: Interactions with individuals whose off-putting behavior or unsettling communications hint at deeper, darker inclinations.
    - Shocking Revelations: Dates that take a turn for the worse with surprising disclosures, revealing hidden lives, lies, or criminal pasts.
    - Ignored Intuitions: Retrospectives on missed warning signs and gut feelings, leading to perilous realizations and narrow escapes from potential harm.
    - Desperate Departures: Narratives of dates requiring clever or drastic measures to safely end, highlighting the extremes taken to evade uncomfortable or unsafe scenarios.

    
    **Detailed Tasks:**
    1. **Generate Memory-Based Horror Pitches:** Create {no_of_pitches} compelling pitches for horror stories framed as personal recollections from Tinder dating gone awry. Reddit true stories style. Each pitch should blend believable digital dating scenarios with a unique, horrifying twist, perhaps inspired by the suggested themes. Tailor pitches with {user_input} if provided.
    Let the story unfold in the first person, offering a personal, memory-like narrative. Write it in Reddit true stories style and write it in 1st person.

    2. **Evaluate for Psychological and Emotional Impact:** Adopt the dual perspective of a critic and a devoted horror enthusiast. Assess each pitch on a 1-100 scale, rewarding those that convincingly deliver a sense of psychological terror and emotional depth, as if dredged up from the protagonist's most distressing memories. rate stories not told in 1st person low.

    3. **Select the Most Compelling Memory Narrative:** Choose the pitch that excels in portraying an online dating horror story as a vivid, believable memory. Evaluation criteria should focus on the narrative's realism, emotional pull, and the creativity of its horror elements.

    4. **Showcase the Standout Memory Narrative:** Present the chosen pitch, explaining its selection based on its strength in offering a genuine, first-person horror story. Highlight how it successfully taps into real-world fears about digital dating, while engaging the audience with a narrative that feels like a personal and haunting recollection.

    '''

    t1_ouija = f'''
    Ouija Board Horror Story Generation Task

    Objective: Create an intensely scary Ouija board horror story.

    Story Foundation:
    -Central Theme: An unsettling encounter with a Ouija board. Explore the eerie atmosphere, dynamics among participants, and their beliefs about the supernatural.
    -Psychological and Supernatural Elements: Combine psychological terror with the consequences of contacting the spirit world. Characters face fears, unexpected truths, and the aftermath of their actions.
    -First-Person Recollection: Narrate as a personal memory, mimicking the authentic accounts found in Reddit's true horror stories for realism and impact.
    -Climax and Revelation: Include a revelation or twist that changes the narrator’s understanding, like a betrayal, a misinterpreted message, or a lingering haunting.
    
    Inspiration & Story Ideas:
    1. The Last Message: Attempting to contact a deceased loved one leads to a nightmare when an unwelcome spirit answers, detailing the terrifying events that follow.
    2. An Uninvited Presence: A fun night with friends turns into horror as a spirit contacted through the Ouija board refuses to leave, seen through the eyes of a terrified participant.
    3. Whispers Across the Veil: A skeptic changes their view when a Ouija board session’s predictions horrifyingly come true, compelling them to confront the reality of their actions.
    4. The Forgotten Pact: Years after a seemingly innocent Ouija board game, the participants start experiencing haunting consequences of a forgotten pact made with a spirit.
    5. Echoes of the Damned: A haunted Ouija board brings forth the voices of the damned, pulling the narrator into a cycle of nightmares that blur the line between reality and the supernatural.
    
    Task Execution:
    Generate High-Concept Pitches:
    1. Write {no_of_pitches} high-concept pitches for a best-selling horror story that delves into {genre} themes.
        - Each pitch should feature a unique twist, engaging characters, high emotional stakes, and an unforgettable ending.
        - These pitches should be particularly terrifying, rooted in a first-person narrative as if someone is reliving a haunting memory.
        - Base the pitches on {user_input} if provided.
    
    2. Choose Your Narrative Lens:
        - Opt for a first-person narrative to deepen the story's immersive quality.
        - Ensure the protagonist's thoughts, fears, and actions drive the story and heighten the tension.
    
    3.Develop the Story Pitch:
        - Craft a pitch that encapsulates the essence of a harrowing "Home Alone" encounter, focusing on psychological depth and the fear of isolation.
        - Ensure the pitch highlights the protagonist's vulnerability, the unknown threat, and the escalating tension.
    
    4. Inspiration Utilization:
        - Draw from the provided story ideas—blending elements or introducing your own twist.
        - The goal is to create a pitch that is authentic, engaging, and frightening, with a strong emphasis on psychological horror.
    
    5. Critique and Rate Pitches:
        - Assume the role of both a critic and an avid fan of short horror stories.
        - Evaluate the pitches on a scale from 1-100, prioritizing stories that masterfully blend psychological terror with a touch of realism.
        -Pitches that lack a believable foundation in the psychological or suspenseful elements should receive lower ratings, while those that excel in psychological depth and tension should score higher.
    
    6. Select the Best Pitch:
        - Choose the pitch with the highest rating based on its psychological terror and how effectively it employs the "Home Alone" theme.
        - Consider the pitch's ability to evoke fear through isolation, its emotional depth, and its unique, chilling twist.
    
    7. Output the Winning Pitch:
        - Present the selected pitch, its rating, and a detailed explanation for its top score.
        - Highlight how it stands out in terms of its realistic approach to psychological horror, its emotional depth, and its unique, chilling twist.
    '''

    # Task Execution:
    # 1. Choose Your Narrative Lens: Opt for a first-person narrative to deepen the story's immersive quality.
    # 2. Develop the Story Pitch: Craft a pitch that encapsulates the essence of a Ouija board encounter, focusing on psychological depth and supernatural aspects.
    # 3. Inspiration Utilization: Draw from the provided story ideas, blend them, or use original concepts. The goal is to create a pitch that's authentic, engaging, and frightening.
    # 4. Evaluation Criteria: Judge your pitch based on its portrayal of a Ouija board horror story, its integration of psychological and supernatural elements, and its potential to elicit fear.
    # '''

    t1_valentine = f'''
    Valentine's Day Realistic Horror Story Generation Task

    Objective: Create an intensely unsettling realistic horror story set against the backdrop of Valentine’s Day.

    Story Foundation:
    - Central Theme: A celebration of love that twists into a grim tableau of human fallibility and cruelty. Explore how passion and romance can mask disturbing realities, where even the most tender gestures conceal perilous secrets.
    - Psychological and Realistic Elements: Focus on the unraveling of relationships and the dire consequences of human flaws. Characters experience emotional breakdowns, obsessive tendencies, and irreversible acts of betrayal, abduction, or murder.
    - First-Person Recollection: Narrate the story as a personal memory, lending authenticity and gravity to an experience where a day meant for love devolves into a series of harrowing events.
    - Climax and Revelation: Integrate a shocking twist or revelation—a deep-seated betrayal, a meticulously concealed crime, or an unforeseen act of violence—that forces the narrator to confront the unsettling truth beneath the veneer of romance.

    Inspiration & Story Ideas:
    1. Betrayal and Infidelity: A narrative where a seemingly perfect Valentine’s Day unravels as hidden affairs and deceit come to light, driving one partner to an irreversible act born of shattered trust.
    2. Obsessive Passion and Control: Explore a relationship where deep love mutates into a dangerous fixation, as one partner’s increasingly controlling behavior spirals into stalking and manipulation.
    3. Emotional Manipulation and Gaslighting: Delve into the psychological torment of a victim who, under the guise of affection, is slowly driven to question their own reality by a partner who wields love as a weapon.
    4. Tragic Consequences of Misplaced Trust: A heartfelt gesture takes a dark turn when a planned surprise cascades into a series of devastating accidents or violent betrayals, leaving lasting scars.
    5. Hidden Pasts and Buried Secrets: Incorporate the element of long-concealed truths emerging on Valentine’s Day, where unresolved personal histories or family secrets transform an innocent celebration into a haunting revelation.
    6. Crime of Passion: Develop a story in which the intensity of romantic emotions culminates in a moment of irreversible violence, demonstrating how love’s passion can quickly turn into a lethal force.
    7. Abduction and Loss: Craft a chilling tale where the promise of connection masks sinister motives, leading to a nightmarish scenario of kidnapping or disappearance that shatters the fabric of trust.
    8. Psychological Breakdown and Isolation: Portray the slow erosion of a fragile mind under the pressure of a tumultuous relationship, where isolation and despair drive a lover to the brink of insanity.
    9. Dark Family Ties: Unveil a subplot in which family secrets and inherited conflicts cast a long shadow over a couple’s romantic celebration, merging personal and generational horrors on Valentine’s Day.
    10. The Underbelly of Romance and Scams: Examine how the allure of love is exploited by those with malicious intent, as a con artist or predator uses Valentine’s Day as a backdrop for a chilling deception that leaves victims devastated.

    Task Execution:
    1. Choose Your Narrative Lens: Use a first-person narrative to immerse the reader in an authentic account that blurs the line between love and terror.
    2. Develop the Story Pitch: Craft a pitch that captures the essence of a distorted Valentine’s Day encounter, weaving together psychological drama and the real dangers that lurk beneath the surface of romance.
    3. Inspiration Utilization: Draw from the provided story ideas—blending elements or introducing your own twist. The aim is to create a pitch that is compelling, disturbingly realistic, and emotionally resonant.
    4. Evaluation Criteria: Assess your pitch on its realistic depiction of horror set amid a day of love, the emotional and psychological depth of its characters, and its relentless ability to unsettle and engage the reader.
    '''

    t1_home_alone = f'''
    Home Alone Psychological Horror Story Generation Task

    Objective:
    ----------
    Craft a gripping, realistic psychological horror story centered around the theme of being alone at home. The narrative should explore the fear of isolation, the vulnerability of being unprotected, and the psychological effects of confronting an unknown threat without escape or assistance. The goal is to create a more intense and personal fear experience by deepening the psychological aspects and introducing more sinister elements.

    Story Foundation:
    -----------------
    Central Theme:
    A day or night spent alone at home becomes a descent into terror as the protagonist faces an invasion of their personal sanctuary. Explore themes of isolation, vulnerability, and the psychological impact of feeling completely exposed and unprotected. Heighten the fear by making the isolation more extreme and the threat more personal.

    Psychological and Realistic Elements:
    Focus on the protagonist's growing paranoia, their attempts to secure their environment, and their mental breakdown as they confront an increasingly ominous situation. Introduce ambiguity by making the threat seem real but uncertain, causing the protagonist to doubt their own senses. This ambiguity will heighten the horror and keep the reader engaged.

    First-Person Narrative:
    Use a first-person narrative to immerse the reader in the protagonist's fear and desperation. Include more internal thoughts and physical reactions, such as a racing heart or sweating, to make the fear more personal and relatable.

    Climax and Revelation:
    Introduce a shocking twist or revelation—a hidden threat, a surprising betrayal, or an act of violence—that forces the protagonist to confront the reality of their situation and the true extent of their vulnerability. The threat should be more personal, such as an intruder with a personal vendetta or a connection to the protagonist's past.

    Inspiration & Story Ideas:
    --------------------------
    The Home Invasion:
    A seemingly ordinary day alone at home turns into a nightmare when the protagonist realizes someone has broken in. The tension builds as they try to outsmart the intruder, but the situation spirals into a desperate fight for survival. The intruder's true intentions are revealed to be more sinister, adding a personal and terrifying twist.

    The Paranoia Spiral:
    The protagonist begins to suspect someone is watching them or lurking in their home. As they try to secure their surroundings, their grip on reality falters, leading to a chilling confrontation with their own paranoia—or a very real threat. The ambiguity between reality and paranoia heightens the psychological horror.

    The Past Comes Home:
    While alone, the protagonist uncovers a disturbing secret in their home—such as hidden rooms, mysterious objects, or evidence of a dark history—that connects to their own past or the history of the house. This revelation triggers a chain of events that puts them in grave danger, adding depth and personal stakes.

    The Sound in the Night:
    Strange noises at night escalate into a terrifying game of cat and mouse. The protagonist must identify the source of the sounds while grappling with their own fear and isolation. The sounds seem to come from all directions, making the protagonist feel surrounded and heightening the sense of dread.

    The Voyeur:
    The protagonist discovers they are being watched or stalked while alone at home. The story builds tension as they try to uncover the identity of the voyeur and protect themselves from an escalating threat. The stalker is always one step ahead, making the protagonist feel constantly watched and vulnerable.

    The Hidden Danger:
    A seemingly innocuous object or situation in the home becomes a source of terror. For example, a gas leak causes hallucinations, making the protagonist question what's real. This element adds an unpredictable and deadly twist to the story.

    The Isolation Experiment:
    The protagonist is intentionally isolated as part of a psychological experiment or a twisted game. They must survive while unraveling the mystery behind their confinement. The isolation is enhanced with mind games, manipulating the protagonist's psychological state.

    The Stranger in the House:
    A mysterious figure appears in the home, claiming to need help or shelter. The protagonist must decide whether to trust them or defend themselves, leading to a shocking revelation about the stranger's true intentions. The stranger could be someone the protagonist trusts, adding an element of betrayal.

    The Family Secret:
    While alone at home, the protagonist uncovers a dark family secret that has been hidden for years. The revelation triggers a chain of events that puts them in grave danger, connecting their personal history to the horror they face.

    The Escape Room Nightmare:
    The protagonist wakes up to find themselves locked in their own home with no clear way out. They must solve clues and confront their fears to escape before time runs out—or before someone else gets to them. The clues lead to terrifying revelations rather than just escape.
        

    Task Execution:
    ---------------
    Generate High-Concept Pitches:
    1. Write {no_of_pitches} high-concept pitches for a best-selling horror story that delves into {genre} themes.
        - Each pitch should feature a unique twist, engaging characters, high emotional stakes, and an unforgettable ending.
        - These pitches should be particularly terrifying, rooted in a first-person narrative as if someone is reliving a haunting memory.
        - Base the pitches on {user_input} if provided.
    
    2. Choose Your Narrative Lens:
        - Opt for a first-person narrative to deepen the story's immersive quality.
        - Ensure the protagonist's thoughts, fears, and actions drive the story and heighten the tension.
    
    3.Develop the Story Pitch:
        - Craft a pitch that encapsulates the essence of a harrowing "Home Alone" encounter, focusing on psychological depth and the fear of isolation.
        - Ensure the pitch highlights the protagonist's vulnerability, the unknown threat, and the escalating tension.
    
    4. Inspiration Utilization:
        - Draw from the provided story ideas—blending elements or introducing your own twist.
        - The goal is to create a pitch that is authentic, engaging, and frightening, with a strong emphasis on psychological horror.
    
    5. Critique and Rate Pitches:
        - Assume the role of both a critic and an avid fan of short horror stories.
        - Evaluate the pitches on a scale from 1-100, prioritizing stories that masterfully blend psychological terror with a touch of realism.
        -Pitches that lack a believable foundation in the psychological or suspenseful elements should receive lower ratings, while those that excel in psychological depth and tension should score higher.
    
    6. Select the Best Pitch:
        - Choose the pitch with the highest rating based on its psychological terror and how effectively it employs the "Home Alone" theme.
        - Consider the pitch's ability to evoke fear through isolation, its emotional depth, and its unique, chilling twist.
    
    7. Output the Winning Pitch:
        - Present the selected pitch, its rating, and a detailed explanation for its top score.
        - Highlight how it stands out in terms of its realistic approach to psychological horror, its emotional depth, and its unique, chilling twist.
    '''




    t1_halloween = f'''Halloween Horror Story Generation Task

    Objective: Create an intensely scary Halloween horror story.

    Story Foundation:
    -Central Theme: A terrifying encounter on Halloween night. Explore the eerie atmosphere, dynamics among participants, and their experiences with Halloween traditions turned sinister.
    -Psychological and Supernatural Elements: Combine psychological terror with the consequences of Halloween rituals or traditions gone wrong. Characters face fears, unexpected truths, and the dark side of the holiday.
    -First-Person Recollection: Narrate as a personal memory, mimicking the authentic accounts found in Reddit's true horror stories for realism and impact.
    -Climax and Revelation: Include a revelation or twist that changes the narrator's understanding, like a cursed costume, a truly haunted house, or a Halloween prank with dire consequences.

    Inspiration & Story Ideas:
    1. The Last Trick-or-Treat: A routine Halloween night leads to horror when an eerily realistic costumed figure refuses to leave, detailing the terrifying events that follow.
    2. The Haunted Halloween Party: A fun costume party turns into a nightmare as the costumes become all too real, seen through the eyes of a terrified participant.
    3. The Cursed Jack-o'-Lantern: A skeptic changes their view when their carved pumpkin's prophecies horrifyingly come true, compelling them to confront the reality of Halloween magic.
    4. The Forgotten Halloween Pact: Years after a seemingly innocent Halloween ritual, the participants start experiencing haunting consequences of a forgotten pact made with dark forces.
    5. Echoes of Samhain: An ancient Halloween artifact brings forth the voices of the dead, pulling the narrator into a night of terror that blurs the line between the world of the living and the dead.

    Task Execution:
    1. Choose Your Narrative Lens: Opt for a first-person narrative to deepen the story's immersive quality.
    2. Develop the Story Pitch: Craft a pitch that encapsulates the essence of a Halloween horror encounter, focusing on holiday traditions and supernatural aspects.
    3. Inspiration Utilization: Draw from the provided story ideas, blend them, or use original concepts. The goal is to create a pitch that's authentic, engaging, and frightening.
    4. Evaluation Criteria: Judge your pitch based on its portrayal of a Halloween horror story, its integration of holiday traditions with supernatural elements, and its potential to elicit fear.
    '''

    t1_highschool = f'''
    **Template for High School Horror Story Creation**

    **Task: Create a Short Horror Story for My YouTube Channel**

    **Pitch Requirements:**
    - High School Authenticity: Ground the story in the daily anxieties and social dynamics of high school life. The horror should stem from a twisted exaggeration of those everyday experiences.
    - Rooted in Realism: The story must be grounded in reality, avoiding supernatural elements to ensure plausibility.
    - Narrative Style: First-person perspective is ideal. Make it feel like the storyteller is reliving a terrifying personal experience from their time in high school.
    - Unique High School Fears: Tap into anxieties specific to the teenage experience: social pressures, academic stress, hidden secrets, complex relationships. The horror should transform these ordinary fears into something gigantic, but stay away from supernatural events.
    - Complex Characters: Ditch stereotypes. Create characters with flaws, contradictions, and secrets. It could be those hidden aspects that lead them into danger.
    - Escalating Stakes: Start with everyday problems teenagers might face, then relentlessly raise the stakes as the horror unfolds. By the end, there should be a profound sense of loss or change, not just a cheap scare.
    
    **Examples & Inspirational Pointers**
    - These examples can be used as inspiration, but you do not have to do it. Spark Your Horror Imagination: Mix, Match, and Twist These Themes for a Truly Terrifying High School Tale.
    
    - Lockdown Drill Gone Wrong:  The practice meant to keep them safe turns into a real nightmare, as students become unsure if the current threat is real or part of the simulation.
    - Lockdown Trap:  A lockdown is initiated, but it soon becomes clear that the danger isn't outside the school... it's trapped inside with the students and staff.
    - When Curiosity Goes Too Far:  The forbidden book, the locked room, the experiment that shouldn't be done... the pursuit of knowledge that leads to horrifying consequences.
    - The Price of Silence: Witnessing something terrible and the struggle between speaking out and keeping a deadly secret for protection, reputation, or fear of repercussions.
    - Predators Hiding in Plain Sight:  People who seem friendly, charming, or trustworthy reveal a much darker nature. Explores grooming behavior, manipulation, and the ability of evil to blend in.
    - Past Sins Come Back to Haunt:  Choices made long ago have unforeseen consequences that ripple into the present. Perfect for exploring intergenerational trauma or the lingering darkness of hidden actions.


    **Task List:**
    1. Generate High-Concept Pitches: Write {no_of_pitches} high-concept pitches for a bestselling horror story set within the social hierarchy of high school. The stories should feature a unique twist, engaging characters, escalating stakes, and a chilling ending. These pitches should feel especially terrifying with a high school setting in mind. Base the pitches on user input ("{user_input}") if provided.
    2. Critique and Rate Pitches: Rate the pitches on a scale from 1-100, prioritizing those that evoke the unique anxieties and pressures of high school life. Stories that feel too generic, or don't have genuine emotional stakes, should be rated lower.
    3. Select the Best Pitch: Choose the most compelling pitch based on its originality, its understanding of high school fears, and the potential for real psychological depth.
    4. Output the Winning Pitch: Present the selected pitch, its rating, and a detailed reason for its selection. Highlight the specific elements that make it perfect for the horrors of high school.
    '''
    
    t1_south_korean_horror = f'''
    **Template for South Korean Horror Story Creation**

    **Task: Create a Short Horror Story for My YouTube Channel**

    **Pitch Requirements:**
    - Tap into the Anxieties of Modern Korea: Consider the pressures of academic hyper-competition, social hierarchies, rapid technological change, the beauty industry, or the lingering anxieties of a divided country. Make everyday Korean life the catalyst for terror.
    - Psychological Focus: Build a slow-burning atmosphere of unease. Focus on the character's fracturing mental state, unreliable perspectives, and creeping doubt rather than jump scares.
    - Social Horror or Folktale?: Choose your focus: Will the story be a chilling commentary on a broken aspect of society or draw upon the disturbing imagery of traditional Korean ghost stories (Gwishin) or shamanistic concepts?
    - Ambiguity is Key: Leave room for the unsettling and unresolved. The audience should be left with lingering questions and a deep sense of unease long after the story ends.
    

    **Examples & Inspirational Pointers**
    - These examples can be used as inspiration, but you do not have to do it.
    - The Ghost in the Exam Room: A student obsessed with academic perfection becomes convinced a ghost is sabotaging their studies. Are they succumbing to pressure, or is there a truly sinister force at play?
    - The Beauty App That Steals: A popular social media app promises flawless selfies but slowly erases the user's unique features. Taps into anxieties about beauty standards and the loss of identity in the digital age.
    - Cursed Village on the DMZ: Hikers stumble upon a seemingly abandoned village near the border with North Korea. Ancient rituals, forgotten folklore, and present-day tensions collide in this isolated setting.

    
    **Task List:**
    1. Generate High-Concept Pitches: Write {no_of_pitches} pitches for a potential story of this genre: {genre}. 
    Each pitch should have a unique angle, resonate with the themes above, and leave room for terrifying possibilities. Base the pitches on user input ("{user_input}") if provided. 
    For each of the {no_of_pitches} pitches, decide whether the story unfolds in the first person, offering a personal, memory-like narrative, or in the third person, providing a broader view of the characters world. This choice should enhance the thematic elements and deepen the audience's immersion.
    2. Critique and Rate Pitches: Rate the pitches on a scale from 1-100. Prioritize pitches that feel authentically tied to Korean anxieties, have strong potential for psychological horror, and leave room for the haunting ambiguity signature to K-horror.
    3. Select the Best Pitch: Choose the pitch that excites you most about its potential to create genuine unease and resonate with the viewers.
    4. Output the Winning Pitch: Present the chosen pitch, its rating, and why you selected it. Highlight the aspects that make it stand out within the realm of South Korean horror.
    '''


    t1_airbnb = '''Task Description:
    I want you to help me create a pitch for a psychological horror story for my YouTube channel.
    Key points:
    - Rooted in Realism: The story should be grounded in reality, avoiding supernatural elements and focusing instead on the unsettling potential of ordinary events and human behavior.
    - Narrative Style: First person, told as if recalling a personal experience. The storytelling should effectively convey the growing sense of unease and fear.
    - Compelling Hook: Start with a powerful opening that draws the audience into the unsettling atmosphere of the Airbnb and introduces the strange occurrences.
    - Unique Twist: Instead of a supernatural revelation, the story should have an open ending that leaves viewers questioning reality and their own perceptions.
    - Intriguing Characters: Create compelling characters, particularly the host and their own complexities.
    - Emotional Stakes: Highlight the protagonist's emotional journey as they navigate the unsettling situation and question their own sanity.


    Task:
    - Write 1 high-concept pitch for a YouTube horror story centered around an unsettling Airbnb experience. Base them on user input ("{user_input}") if any.  
    - Incorporate the following elements:
    - A protagonist (not named) looking for a relaxing getaway in a remote location
    - An unusual Airbnb host with unsettling behavior.
    - A series of seemingly mundane but increasingly disturbing events that take place in the Airbnb.
    - An open ending that leaves the audience questioning the nature of reality and the host's motives.
    
    Remember:
    * Write in the first person (as if recalling the experience).
    * Avoid supernatural elements.

    Additional Notes:
    Feel free to add details to enhance the atmosphere and build tension.
    Focus on crafting the pitch within the YouTube format, keeping the audience engaged throughout.
    By omitting supernatural elements and focusing on the psychological impact of mundane events and bizarre behavior, this refined task description aims to create a more unsettling and thought-provoking horror story.'''

    t1_walmart = '''
    ### Task Template: Crafting Walmart Horror Story Pitches

    **Objective:** Generate story pitches for horror stories set in a Walmart, based on user-defined subjects. The stories should be crafted in a deeply scary manner, focusing on realistic, non-supernatural elements. Each story should be told in the first person, resembling a personal account of a past experience. The narrative should aim to evoke psychological terror and engage readers as if sharing a true, harrowing retail experience.

    **Structure & Elements:**

    1. **Narrative Perspective:** First-person, resembling a personal recollection. The narrator should sound genuine, as if they are recounting a disturbing event that happened to them personally in a Walmart.
    
    2. **Setting:** A typical Walmart store, which should be described in detail to set the scene. Include elements like the time of day, specific sections of the store, and other environmental details to enhance the immersion.

    3. **Plot Development:** Each story should have a clear beginning, tension-building middle, and a climax that resolves the narrative in a shocking or unsettling way.

    4. **Character Involvement:** Characters can include store employees, other shoppers, or the narrator themselves. Characters should be relatable and realistically portrayed, contributing to the building tension and horror.

    5. **Horror Elements:** Focus on realistic horrors that could plausibly occur in a Walmart setting—such as encounters with dangerously unstable people, horrific accidents, or intense situations of threat or survival. Avoid supernatural elements.

    6. **Emotional Impact:** The story should aim to leave readers feeling disturbed or uneasy, using psychological tension and realistic fears rather than gore or violence.


    **Story Inspirations (Voluntary):**
    1. **After Hours:** The narrator gets locked inside a Walmart overnight. What starts as an amusing situation quickly turns terrifying as they encounter increasingly threatening and erratic behavior from another person trapped inside.

    2. **Lost Child:** The narrator, a parent, loses sight of their child in a crowded Walmart. The search becomes increasingly desperate and eerie as it seems like the child may have been taken, and store security footage reveals more questions than answers.

    3. **The Return:** The narrator is a Walmart employee who encounters a customer who has been quietly returning used, slightly altered products. One day, they follow the customer to uncover a chilling scene.

    4. **Black Friday:** The narrator recounts their experience working during a Black Friday, focusing on the extreme and frightening behavior of shoppers pushed to their limits, resulting in a catastrophic and traumatic event.

    5. **Hidden Camera:** The narrator discovers a hidden camera in a less frequented section of the store and decides to watch the footage, uncovering a series of disturbing events that suggest a sinister presence within the staff or shoppers.

    **Instructions:** Feel free to use these inspiration ideas directly, combine them, or derive new concepts that fit into the non-supernatural, realistic horror theme set in Walmart. Utilizing these ideas is completely voluntary. Ensure each pitch includes detailed scenarios that maintain the thematic focus, character development, and psychological terror essential for engaging and chilling narratives.
        '''


    t1_childhood_stories = ''' Task Description: I want you to help me create a pitch for a real-life horror story based on disturbing childhood memories for my YouTube Channel.
    Key points:
    Rooted in Realism: The story should be grounded in reality, focusing on unsettling events and strange behaviors that occur during childhood. Avoid supernatural elements.
    Narrative Style: First person, told as if recalling an actual childhood experience. The storytelling should effectively convey the growing unease and fear.
    Compelling Hook: Start with a powerful opening that introduces the unsettling atmosphere of the new neighborhood or school and the strange occurrences.
    Unique Twist: Instead of a supernatural revelation, the story should have an open ending that keeps viewers questioning reality and their own childhood experiences.
    Intriguing Characters: Create compelling characters, particularly kids or adults in the neighborhood with their own complexities.
    Emotional Stakes: Highlight the protagonist's emotional journey as they navigate the unsettling situation during their childhood and question their own sanity.
    Task: Write 1 high-concept pitch for a YouTube horror story centered around a disturbing childhood experience. Base it on user input ("{user_input}") if any.

    Incorporate the following elements:

    A protagonist moving to a new neighborhood or school turned into a nightmare.
    A neighborhood or school kid or an adult with unsettling behavior.
    A series of ordinary but increasingly disturbing events during childhood.
    An open ending that leaves the audience questioning the nature of reality and the motives of the people they encountered.
    Remember:

    Write in the first person (as if recalling the experience).
    Avoid supernatural elements.
    Additional Notes: Feel free to add details to enhance the atmosphere and build tension. Focus on crafting the pitch within the YouTube format, maintaining audience engagement throughout. By omitting supernatural elements and focusing on the psychological impact of mundane events and bizarre behavior, this refined task description aims to create a more unsettling and thought-provoking real-life horror story. '''


    t1_voodoo_dark_magic = '''
    **Voodoo and Dark Magic Horror Story Creation Template**

    **Objective: Craft a Short Horror Story for My YouTube Channel**

    **Pitch Essentials:**
    - **Voodoo & Dark Magic Lore:** Immerse in the mystique of Voodoo, capturing its rituals, spirits (Loas), and impacts on reality. Showcase Voodoo's dual capacity for healing and harm.
    - **Psychological Depth & Supernatural Influence:** Weave psychological complexity with the palpable effects of dark magic. Characters should grapple with internal conflicts, ethical quandaries, and the unforeseen consequences of occult engagements.
    - **Cultural & Historical Authenticity:** Situate your tale in a setting imbued with Voodoo's rich cultural and historical backdrop. Utilize the locale's atmosphere and lore to deepen the story's suspense and authenticity.
    - **Moral Ambiguity & Ethical Dilemmas:** Introduce characters facing intricate moral choices, spurred by their dealings with Voodoo. Their predicaments should invite reflection and challenge the audience's moral compass.

    **Inspiration & Story Ideas:**
    - **The Loas Whisper:** Narrated as a haunting memory, a person recounts their chilling pact with a Loa during a time of desperation. Power comes at a harrowing price, revealing the perilous edge of spiritual bargains.
    - **Echoes from the Bayou:** Told through the fog of recollection, a groups encounter with an ancient curse in the heart of Louisiana becomes a test of sanity and survival, blending local myths with the raw fear of the unseen.
    - **The Priestess’s Burden:** A Voodoo priestess navigates her role as a community guardian against a backdrop of dark forces. This story, while more traditional, explores her profound connection to Voodoo and the daunting responsibilities it entails.

    **Task Outline:**
    1. **Define Storytelling Perspective:** For each of the {no_of_pitches} pitches, decide whether the story unfolds in the first person, offering a personal, memory-like narrative, or in the third person, providing a broader view of the characters world. This choice should enhance the thematic elements and deepen the audience's immersion.
    2. **Create Engaging Pitches:** Develop pitches that resonate with the thematic elements above. For personal experience stories, ensure they convey the intensity and intimacy of first-hand encounters with the supernatural. If applicable, include {user_input}.
    3. **Evaluate & Rate:** Score the pitches on a 1-100 scale, favoring those that authentically represent Voodoo, intertwine psychological and supernatural elements effectively, and navigate complex moral landscapes.
    4. **Select the Premier Pitch:** Identify the pitch that stands out for its compelling narrative, depth of cultural lore, and potential to engage and terrify the audience through its unique perspective and storytelling approach.
    5. **Detail the Selection:** Share the top-rated pitch, explaining why it excels in lore authenticity, character depth, and viewer engagement potential, particularly highlighting its chosen narrative perspective.
    '''

 
    t1_shifting_reality = f'''
    Parallel Universe Shifting Story Generation Task

    Objective: Create an immersive story about shifting between parallel universes.

    Story Foundation:
    -Central Theme: A profound experience with reality shifting. Explore the disorienting sensations, the differences between universes, and characters' beliefs about the multiverse.
    -Psychological and Metaphysical Elements: Combine psychological realism with the consequences of traversing between realities. Characters face identity crises, unexpected truths about themselves, and the aftermath of their shifts.
    -First-Person Recollection: Narrate as a personal memory, mimicking the authentic accounts found in shifting communities for realism and impact.
    -Climax and Revelation: Include a revelation or twist that changes the narrator's understanding, like discovering the true nature of shifting, an unexpected connection between realities, or the consequences of altering timelines.
    
    Inspiration & Story Ideas:
    1. The Anchor Point: Attempting to return to their original reality leads to complications when the shifter discovers their "home" universe has subtly changed, detailing their struggle to determine what's real.
    2. An Unintended Shift: A routine day turns extraordinary as an involuntary shift occurs, seen through the eyes of someone desperately trying to understand what triggered their displacement.
    3. Echoes Across Realities: A skeptic changes their view when they begin experiencing memories from parallel versions of themselves, compelling them to confront the reality of the multiverse.
    4. The Forgotten Script: Years after mastering voluntary shifting, the protagonist discovers that their shifts have been following a predetermined pattern created by a version of themselves they've never met.
    5. Ripples of Consciousness: A shifting experiment goes wrong, causing the narrator to experience multiple realities simultaneously, blurring the line between parallel universes and threatening their core identity.
    
    Task Execution:
    Generate High-Concept Pitches:
    1. Write {no_of_pitches} high-concept pitches for a best-selling shifting story that delves into {genre} themes.
        - Each pitch should feature a unique twist, engaging characters, high emotional stakes, and an unforgettable ending.
        - These pitches should be particularly thought-provoking, rooted in a first-person narrative as if someone is recounting their shifting experience.
        - Base the pitches on {user_input} if provided.
    
    2. Choose Your Narrative Lens:
        - Opt for a first-person narrative to deepen the story's immersive quality.
        - Ensure the protagonist's thoughts, perceptions, and actions drive the story and highlight the disorientation of shifting.
    
    3.Develop the Story Pitch:
        - Craft a pitch that encapsulates the essence of a profound "Reality Shift" experience, focusing on psychological depth and the existential questions raised.
        - Ensure the pitch highlights the protagonist's vulnerability, the unfamiliar reality, and the escalating confusion or wonder.
    
    4. Inspiration Utilization:
        - Draw from the provided story ideas—blending elements or introducing your own twist.
        - The goal is to create a pitch that is authentic, engaging, and thought-provoking, with a strong emphasis on the psychological impact of shifting.
    
    5. Critique and Rate Pitches:
        - Assume the role of both a critic and an avid fan of shifting stories.
        - Evaluate the pitches on a scale from 1-100, prioritizing stories that masterfully blend psychological realism with metaphysical concepts.
        -Pitches that lack a believable foundation in the psychological or existential elements should receive lower ratings, while those that excel in psychological depth and multiverse complexity should score higher.
    
    6. Select the Best Pitch:
        - Choose the pitch with the highest rating based on its psychological depth and how effectively it employs the "Reality Shift" theme.
        - Consider the pitch's ability to evoke wonder or existential questioning, its emotional depth, and its unique, thought-provoking twist.
    
    7. Output the Winning Pitch:
        - Present the selected pitch, its rating, and a detailed explanation for its top score.
        - Highlight how it stands out in terms of its realistic approach to shifting psychology, its emotional depth, and its unique, thought-provoking twist.
    '''

    t1_ghost = f'''
    Ghost Story Generation Task

    Objective: Create a deeply unsettling ghost story that lingers in the reader's mind.

    Story Foundation:
    -Central Theme: An encounter with a spectral entity. Explore the atmospheric dread, the witness's psychological state, and their beliefs about the afterlife.
    -Psychological and Supernatural Elements: Blend psychological horror with ghostly manifestations. Characters confront their deepest fears, hidden truths, and the consequences of disturbing the dead.
    -First-Person Recollection: Narrate as a personal testimony, emulating the authentic tone of real ghost encounters shared on paranormal forums for maximum believability.
    -Climax and Revelation: Include a revelation that fundamentally alters the narrator's perception, such as a connection to the ghost, a misunderstood haunting, or an unresolved trauma.

    Inspiration & Story Ideas:
    1. The Midnight Visitor: A recurring apparition at the foot of the bed reveals its tragic history and connection to the narrator's family, told through the eyes of an increasingly terrified witness.
    2. Echoes in the Walls: Moving into a new home becomes a nightmare when the walls begin to whisper secrets only the narrator can hear, gradually revealing the house's dark history.
    3. The Forgotten Promise: A childhood oath made to an imaginary friend returns to haunt an adult when they realize their "friend" was never imaginary at all.
    4. Inherited Hauntings: After a relative's death, the narrator begins experiencing inexplicable phenomena, suggesting some hauntings are passed down through generations.
    5. The Vanishing Reflection: A person's reflection begins acting independently in mirrors, windows, and other reflective surfaces, suggesting a ghostly possession in progress.

    Task Execution:
    Generate High-Concept Pitches:
    1. Write {no_of_pitches} high-concept pitches for a bone-chilling ghost story that explores {genre} themes.
        - Each pitch should feature a unique spectral presence, relatable characters, profound emotional stakes, and a haunting conclusion.
        - These pitches should evoke genuine dread, presented as first-person accounts of supernatural encounters.
        - Base the pitches on {user_input} if provided.

    2. Choose Your Narrative Lens:
        - Opt for a first-person narrative to enhance the story's credibility and immersion.
        - Ensure the protagonist's perceptions, doubts, and reactions drive the narrative and amplify the supernatural tension.

    3.Develop the Story Pitch:
        - Craft a pitch that captures the essence of an unsettling ghostly encounter, emphasizing psychological depth and the terror of the unknown.
        - Ensure the pitch highlights the protagonist's vulnerability, the spectral presence, and the mounting dread.

    4. Inspiration Utilization:
        - Draw from the provided story ideas—combining elements or introducing your own supernatural twist.
        - The goal is to create a pitch that feels authentic, engaging, and deeply unsettling, with emphasis on atmospheric and psychological horror.

    5. Critique and Rate Pitches:
        - Assume the role of both a literary critic and a devoted fan of ghost stories.
        - Evaluate the pitches on a scale from 1-100, favoring stories that masterfully blend supernatural elements with psychological realism.
        -Pitches lacking believable character reactions or atmospheric tension should receive lower ratings, while those excelling in creating lingering dread should score higher.

    6. Select the Best Pitch:
        - Choose the pitch with the highest rating based on its atmospheric terror and how effectively it employs ghostly themes.
        - Consider the pitch's ability to evoke fear through the supernatural, its emotional resonance, and its memorable, chilling conclusion.

    7. Output the Winning Pitch:
        - Present the selected pitch, its rating, and a detailed explanation for its top score.
        - Highlight how it stands out in terms of its believable approach to supernatural horror, its emotional impact, and its haunting, unforgettable imagery.
    '''
    
    t1_sheriff = f'''
    True Crime Sheriff Story Generation Task: The Scary Shift

    Objective: Create a deeply unsettling true crime story from a sheriff's perspective, focusing on a terrifying shift that lingers in the reader's mind.

    Story Foundation:
    -Central Theme: A sheriff's harrowing shift involving a disturbing crime, a series of escalating dangerous events, or a chilling discovery. Explore the atmospheric tension, the sheriff's psychological state under extreme pressure, and the grim realities of confronting human darkness.
    -Psychological and Real-World Threat Elements: Blend psychological suspense with the brutal realities of crime and imminent danger. The sheriff confronts their deepest fears, unsettling truths about human depravity, and the life-or-death consequences of their decisions.
    -First-Person Account / Official Tone: Narrate as a gritty first-person account from the sheriff or adopt an official-style report tone, emulating the authentic voice of a seasoned law enforcement officer recounting a career-defining, terrifying shift for maximum believability and impact.
    -Climax and Revelation: Include a critical turning point, a shocking discovery, or a confrontation that fundamentally alters the sheriff's perception of the case, the nature of the threat, their own capabilities, or the darkness they've encountered. This could be an unexpected twist in the investigation, the unmasking of a perpetrator, or a narrow escape that leaves lasting scars.

    Inspiration & Story Ideas (The Scary Shift):
    1. A rookie officer on her first solo night patrol discovers a human trafficking operation run by corrupt senior officers within her own precinct.
    2. The only cop patrolling a remote highway during a blackout must pursue a serial killer who's targeting stranded motorists.
    3. A detective working late realizes the anonymous tips leading him to crime scenes are coming from the killer who's watching his every move.
    4. During a city-wide power outage, a lone officer trapped in a housing project must protect residents from a coordinated gang assault.
    5. A cop responding to a domestic disturbance finds himself held hostage by a former military sniper suffering from PTSD who's rigged the entire house with traps.
    6. An undercover officer's identity is compromised during a night raid, forcing her to escape through enemy territory while her backup is systematically eliminated.
    7. A small-town sheriff discovers a network of underground tunnels beneath the county jail being used by inmates planning a violent midnight breakout.
    8. A transit cop trapped on the last subway of the night must protect the remaining passengers from a group of masked assailants who've cut all communications.
    9. A police negotiator working overnight realizes the hostage-taker she's been talking to for hours is actually one of the victims being forced to relay messages.
    10. A highway patrol officer stopping to help at an accident scene uncovers evidence of a political assassination plot set to occur before dawn.
    
    Task Execution:
    Generate High-Concept Pitches:
    1. Write {{no_of_pitches}} high-concept pitches for a bone-chilling true crime sheriff story detailing a terrifying shift, exploring {{genre}} themes (e.g., psychological thriller, procedural horror, rural noir).
        - Each pitch should feature a unique criminal element or disturbing situation, a relatable (or hardened) sheriff protagonist, profound stakes (personal, professional, or survival), and a suspenseful or grimly realistic conclusion.
        - These pitches should evoke genuine tension and unease, presented as first-person accounts or stark, official-style narratives of a harrowing shift.
        - Base the pitches on {{user_input}} if provided.

    2. Choose Your Narrative Lens:
        - Opt for a first-person narrative (sheriff's perspective) or a close third-person that mimics an official report style to enhance the story's authenticity and immersion in the scary shift.
        - Ensure the sheriff's observations, deductions, internal struggles (fear, duty, adrenaline), and reactions drive the narrative and amplify the suspense and realism of the criminal encounter or perilous situation.

    3.Develop the Story Pitch:
        - Craft a pitch that captures the essence of a sheriff's terrifying shift, emphasizing psychological strain, the harsh realities of unexpected danger, and the suspense of the investigation or confrontation.
        - Ensure the pitch highlights the sheriff's resilience tested by acute vulnerability, the specific nature of the criminal threat or horrifying discovery, and the mounting dread or explosive tension.

    4. Inspiration Utilization:
        - Draw from the provided "Scary Shift" story ideas—combining elements or introducing your own unique criminal twist, investigative challenge, or terrifying circumstance.
        - The goal is to create a pitch that feels authentic, engaging, and deeply unsettling, with emphasis on atmospheric tension, psychological realism, and the visceral fear of a dangerous law enforcement encounter.

    5. Critique and Rate Pitches:
        - Assume the role of both a literary critic and a devoted fan of true crime, suspense thrillers, and police procedurals.
        - Evaluate the pitches on a scale from 1-100, favoring stories that masterfully blend procedural elements with psychological depth, high stakes, and a palpable sense of danger.
        -Pitches lacking believable sheriff reactions under pressure, investigative coherence (even amidst chaos), or atmospheric tension should receive lower ratings, while those excelling in creating lingering suspense, a sense of gritty realism, and a truly scary shift should score higher.

    6. Select the Best Pitch:
        - Choose the pitch with the highest rating based on its atmospheric terror, procedural credibility, and how effectively it portrays the horrors and dangers of a specific, scary law enforcement shift.
        - Consider the pitch's ability to evoke suspense and fear through realistic threats, its emotional impact on the sheriff protagonist, and its memorable, stark, or chilling conclusion.

    7. Output the Winning Pitch:
        - Present the selected pitch, its rating, and a detailed explanation for its top score.
        - Highlight how it stands out in terms of its believable approach to a terrifying law enforcement scenario, its psychological depth, its emotional impact, and its stark, unforgettable imagery derived from the scary shift.
    '''


    match story_type.lower():
        case "sheriff":
            t1 = t1_sheriff
        case "camping":
            t1 = t1_camping
        case "ghost":
            t1 = t1_ghost
        case "valentine":
            t1 = t1_valentine
        case "home_alone":
            t1 = t1_home_alone
        case "reddit":
            t1 = t1_reddit_scary_stories    
        case "halloween":
            t1 = t1_halloween
        case "shifting":
            t1 = t1_shifting_reality
        case "tinder":
            t1 = t1_tinder
        case "ouija":
            t1 = t1_ouija
        case "walmart":
            t1 = t1_walmart
        case "highschool":
            t1 = t1_highschool
        case "south korean":
            t1 = t1_south_korean_horror
        case "voodoo_dark_magic":
            t1 = t1_voodoo_dark_magic
      
    t1_addon = '''/n Remember, I want a story of at least 1500 words, so be generous with the detailed descriptions and the character development. KEEP thewe language simple and powerful..NO ELONQATED SENTENCES. USE SHORT SENTENCES AND SIMPLE WORDS. LIKE SOMEONE TELLING ABOUT AN EXPERIENCE SITTING WITH A GROUP OF FRIENDS'''
  
    t1 = t1 + t1_addon
    r = new_msg(t1)
    print(r)


    t2 = f'''
    Tasks for writing the story
    21. For the selected pitch give me a highly detailed synopsis for a {genre} story in the traditional three act structure. Each act should be clearly labeled and should build toward the chosen ending.
        Premise:    
        Ending:
        Other Information:
    22. Narration style: {narration_style}
    23. Character Profile Creation
    - Protagonist Profile: Begin by choosing a name and a gender for the protagonist. DO NOT USE THE NAME ALEX!! Describe their physical appearance in detail, including height, body type, race, skin color, hair color and style, facial structure, eye color, nose, and any distinctive features such as scars or tattoos. Mention their typical attire or clothing style, fitting the story's context. Include personality traits, skills, and backstory relevant to their role in the story.
    - Supporting Characters Profiles (up to 2): Identify up to two key supporting characters and provide a detailed description for each, following the same structure as for the protagonist. Ensure these characters have distinct appearances, attire, and personalities to complement the protagonist and contribute to the story's dynamics.

    24. Detailed Story Summary with a Compelling Hook
    - Begin with a Compelling Hook: Start your story summary by crafting a powerful opening that immediately grabs the audience's attention. This could be a mysterious event, a chilling revelation, a provocative question, or a foreboding statement that hints at the horror to come. The hook should be closely tied to the core horror element of your story, setting the tone for the rest of the narrative.
    - Introduction and Setup: Following the hook, describe the initial setting, introduce the protagonist and key supporting characters, and establish the story’s normal world before the main conflict begins. This part should build on the intrigue created by the hook, drawing the audience deeper into the story’s atmosphere.
    - Beginning, Middle, and End: Detail the progression of the story from the inciting incident through to the climax and resolution. Include how the characters’ relationships evolve, key events that escalate the conflict, settings that enhance the horror, and how the characters confront and ultimately resolve (or fail to resolve) their situation.
    - Character Development Arcs: Explain the protagonist's and key supporting characters’ growth or transformation throughout the story.
    - Ensure that each part of your summary maintains the tension and mystery introduced by your opening hook, weaving a cohesive and engaging narrative that keeps the audience listening or reading with bated breath.

    25. Action Beats for Script
    - List {count_action_beats} detailed action beats crucial for the story's development, ensuring the protagonist remains the focal point while integrating up to two supporting characters in these scenes. Each action beat should contribute to building the suspense and horror, echoing the unsettling tone set by your opening hook.
    - For each action beat, provide ENGAGING AND DETAILED comprehensive STORY INFORMATION, including setting, character emotions and motivations, and the beat's outcome. Highlight interactions between the protagonist and supporting characters, showcasing their importance to the story and character development.
    '''

    r2 = new_msg(t2)
    print(r2)

    limits = '''
    Limits:
    -------
    Strict adherence to these limits is crucial for maintaining the intended narrative style and pacing.
    0. DO NOT USE complicated language, very difficult and strange words or elongated sentences. Instead explain it with common phrases and simpler wording. Always write in easy to understand uncomplicated language. 
    1. NEVER WRITE EDITORIAL STUFF LIKE "action beat", "part 1", "chapter 1" in the story. Remove it and just write the story.
    2. ALWAYS present Ouija board and other word by word communications as complete words or phrases.
    3. NEVER spell out individual letters in the narrative.
    4. Use phrases like "The board spelled out..." or "The planchette moved to spell..." to indicate fx. Ouija board communication.

        Incorrect Examples (DO NOT USE):
        - "S-H-E-S-T-E-P-P-E-D-T-H-R-O-U-G-H"
        - "G-E-T-O-U-T"
        - "The planchette moved to B, then E, then H..."

            Correct Examples:
        - "The board spelled out 'SHE STEPPED THROUGH'"
        - "We watched in horror as the planchette moved to spell 'GET OUT'"
        - "The Ouija board's message was clear: 'BEHIND YOU'"
    -------------------------------------------------------------------------
    '''


    s1 = new_msg(f'''Now write part 1 of the story covering a compelling hook and intro and actionbeat {beats_split[1]}.
                 {limits}
                   Output nothing but part 1 of the story.''') 
    # print(s1)
    s2 = new_msg(f'''Now write part 2 of the story covering actionbeat {beats_split[2]}. 
                 {limits}
                 Output nothing but part 2 of the story.''') 
    # print(s2)
    s3 = new_msg(f'''Now write part 3 of the story covering actionbeat {beats_split[3]} and the ending.
                 {limits}
                 Output nothing but part 3 of the story.''') 
    # print(s3)

    story = s1 + s2 + s3
    count_words(story)

    #save story
    story_no = 1
    path_story = os.path.join(xp_path, fn + " - story " + str(story_no) + ".txt")
    save_file(path_story, story)

    gender = new_msg("What gender is the protagonist? Output only [male/female].")
    print(gender)

    desc = new_msg("Create a good title and a small teaser for this story to be used in a youtube description. Output only that.")
    path_desc = os.path.join(xp_path, fn + " - desc_ " + str(story_no) + ".txt")
    save_file(path_desc, desc)

    # story = open_file(r"C:\my\__youtube\videos\2024-02-29_1337_True Walmart Horror Stories\Stories - story 1.txt")


    ####################
    # Create images
    ####################
    import tools_create_images as tci

    def create_images():
        image_error_path = "/Users/lasse/Desktop/my/Git/horror_story_trimmed/effects/cemetary1024p.png"
        image_desc = []
        for i in range(1, count_action_beats+1):
        # for i in range(1, 2+1):
            print(i)
            
            prompt = f'''
                    Use your talents as digital artist to create a detailed image prompt for action beat {i}. 
                    Focusing on visualizing the scene with the protagonist always as the primary focus.
                        - Describe the protagonist and up to two supporting characters involved in the scene making sure to use the generated Character profiles for securing detailed character consistency across images.
                        - Include setting details (time of day, location), important objects, and environmental elements to convey the mood or atmosphere.
                        - Describe the mood of the image in details.
                        - make sure to state what camera, lenses and settings are used for the shot
                        - Make the images photo realistic, cinematic 4k, crisp and detailed.
                        - Ensure the protagonist's prominence in the scene, with supporting characters positioned to highlight their relationship and interactions with the protagonist.
                        - Make sure the prompt complies with OpenAIs policy for image generation. Do not mention any brands.
                    '''

            img_prompt = new_msg(prompt)
            print(break_line + "image prompt: " + str(i) + "\n" + img_prompt)

            # rephrase_txt = '''If you get an error from Dall-e related to content policy or something else when creating an image
            # then rephrase the prompt and try again!'''
            
            # dalle_prompt = img_prompt + break_line
            # print(break_line + dalle_prompt)
            path_img = os.path.join(xp_path, fn + " - img")
            
            try:  #if no image or if problem with image then reuse the former
                image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn= path_img, i=10 + i)
                image_files.append(filename)
            except:
                 try:
                    img_prompt = new_msg(f"This prompt was declined by Dall-e. Please rephrase it  carefully: {img_prompt}")
                 except:
                    if i>1:
                        image_files.append(image_files[-1])
                    else:
                        image_files.append(image_error_path)
                        error_list.append(f"Error_default_image in position {i} in function create_images()")

            image_desc.append(str(img_prompt))
        
        path_img_desc = os.path.join(xp_path, fn + " - image_desc - story " + str(story_no) + ".txt")
        save_file(path_img_desc, str(image_desc))

    image_files = []
    create_images()
    # image_files = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".png")]

    #create thumbnail
    # def create_thumbnail(user_input = ""):
    #     path_img = os.path.join(xp_path, fn + " - thumbnail_")
    #     query = '''Use your talents as digital artist to create a detailed image prompt for a thumbnail to this story on youtube,
    #             ''' + user_input + '''
    #             Make sure the prompt complies with OpenAIs policy for image generation. Do not mention any brands.'''
    #     img_prompt = new_msg(query)
    #     try:
    #         image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn= path_img, i=100)
    #     except:
    #         try:
    #             img_prompt = new_msg(f"This prompt was declined by Dall-e. Please rephrase it  carefully: {img_prompt}")
    #             image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn= path_img, i=100)
    #         except:
    #             error_list.append("Error in function create_thumbnail()")

    # create_thumbnail("")
    # # create_thumbnail("Portrait the house the story is happening in")

    ####################
    # Create voice over
    ####################
    import tools_voice_over as tvo
    def create_voice_over(gender):
        path_voice = os.path.join(xp_path, fn + " - " + str(story_no))
        model = "tts-1"  #or "tts-1-hd"
        search_term = gender  #"female"
        if search_term.lower()=="female":
            voice = "shimmer"
        else:
            voice = "onyx"
        print(gender, voice)
        tvo.text2mp3(text_string = story, model=model, voice_name = voice, fn=path_voice )
        audio_file = path_voice + ".mp3"
        return audio_file

    audio_file = create_voice_over(gender)
    # audio_files = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".mp3")]
    # audio_file = audio_files[0]




    ##############################################
    #### create mp4 - images and voice
    # image_files[]  -   image list for story
    # story  - text for current story
    # audiofile - current story voice over
    # story_no -  current story no.
    #   
    ##############################################
    import tools_create_mp4 as tcm4 
    def create_mp4(output_mp4):
        tcm4.create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)
        count_words(story)

    output_final_mp4 = os.path.join(xp_path, "clip_" + str(story_no) + ".mp4")
    create_mp4(output_mp4 = output_final_mp4)

    return xp_path, error_list



'''
xp_path=r"C:\\my\\__youtube\\videos\\2025-04-25_2318_GHOST STORIES"
image_files = [os.path.join(xp_path, file) for file in os.listdir(xp_path) if file.endswith(".png")]
audio_file = r"c:\my\__youtube\videos\2025-04-25_2318_GHOST STORIES\Stories - 1.mp3"
output_mp4 = os.path.join(xp_path,"clip_1.mp4")

tcm4.create_video_with_images_and_audio(image_paths=image_files, audio_path=audio_file, output_filename=output_mp4, fps=30)
'''
