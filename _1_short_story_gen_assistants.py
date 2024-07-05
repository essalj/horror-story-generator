
#pip install Pillow
# pip install pydub


import re
import os
import openai
from openai import OpenAI
from time import time,sleep
import datetime

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
    gpt4 = "gpt-4o"
    # gpt4 = "gpt-4-turbo"
    gpt3 = "gpt-3.5-turbo"
    selected_gpt = gpt4


    narration_style = "Opt for a first-person narrative to deepen the story's immersive quality."
    # narration_style = "Choose what you think suits the story best."
    fn = "Stories"  #file name
    beats_split = ['7','1-2','3-5','6-7']  # count. part 1, 2, 3
    # beats_split = ['6','1-2','3-4','5-6']  # count. part 1, 2, 3
    count_action_beats = int(beats_split[0])


    no_of_pitches = 3 # to select the best story
    
    
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
    xp_path_0 = "C:\\my\\__youtube\\videos"
    additional_text = genre  # Replace with your desired text
    xp_path = create_dated_folder(xp_path_0, additional_text)
    # print(xp_path)
    # xp_path = r"C:\my\__youtube\videos\2024-02-29_1337_True Walmart Horror Stories"

    ###################
    # Define chatbot
    ###################
    break_line = "\n" + 50*"-" + "\n"

    openai_api_key = open_file('c:\\my\\git\\api-keys\\openaiapikey.txt')
    client = OpenAI(api_key=openai_api_key)
    system_role = open_file("chatbot_horror_writer_role.txt")
    # task = open_file("assistant_horror_task.txt")
    sleep(5)



    #1. create assistant
    assistant = client.beta.assistants.create(
        # instructions="You are a helpful assistant and a master of creating short horror stories",
        instructions = system_role,
        tools=[{"type": "code_interpreter"}],
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
            instructions="Please address user as Sir. Refrain nfrom using the name Alex in the stories you write"
        )

        #Check the run status
        tt = 0
        while True:
            t0 = 5
            tt = tt + t0
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print(f"Run status:{run.status} - " + str(tt) + " seconds.")
            if run.status=='completed':
                break
            sleep(t0)

        #Display messages when run completes
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value  # gets newest reponse from thread
        # print(response)
        return response
    # r = new_msg("What is the gender of the protagonist")
    # print(r)

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

    t1_tinder_old = f'''
    **Template for Creating Tinder Dating Horror Stories**

    **Task: Craft a Short Horror Story for My YouTube Channel**

    **Pitch Requirements:**

    **Rooted in Digital Dating Realism:** The story should delve into the eerie and unsettling experiences within the world of Tinder dating, portraying scenarios that are plausible and resonant with the realities of digital dating, yet tinged with horror.

    **Narrative Style:** The narrative should be presented in the first person, offering an intimate recounting of a Tinder dating experience gone horribly wrong. This style should immerse the audience, making them feel as if they're listening to a friend share a deeply personal and terrifying story.

    **Unique Dating Twist:** Incorporate a unique twist that transforms an ordinary Tinder date into an unforgettable horror story. This twist should be innovative and heighten the sense of dread, setting your story apart from typical dating horror tales.

    **Complex Characters on Tinder:** Craft characters that are rich in depth and intricacy, with their motivations, backgrounds, and actions driving the narrative forward. Their interactions through Tinder should be central to the story, adding layers of complexity and suspense.

    **High Emotional Stakes:** Build the story with significant emotional investment, where the stakes are personal and potentially devastating. The emotional journey should be compelling, intensifying the horror of the dating experience and making the story resonate on a deeper level.

    **Commmon Themes:**
     - "Catfishing dangers, cult entrapment, deceitful web, escape challenge."
     - "Baited Hook, Online dating scam, emotional manipulation, financial exploitation, malevolent     scheme."
     - "Blackmail horror, intimate deception, digital betrayal, ransom demand."
     - "Tinder Horror, Date gone wrong, unexpected danger, escalating fear."
    
    
    Task List:

    1. Generate High-Concept Pitches: Write {no_of_pitches} high-concept pitches for a captivating horror story set against the backdrop of Tinder dating. Avoid using the name Alex for the characters. Draw inspiration from the common themes.Each pitch should be very realistic and believable so that no one doubts that it could be true. It should boast a unique twist, engaging characters, high emotional stakes, and a memorable ending that leaves the audience chilled. The narratives should be particularly harrowing, told in the first person to emphasize the personal horror of the dating experience. Include {user_input} for personalized pitches, if provided.

    2. Critique and Rate Pitches: Take on the dual roles of critic and enthusiastic fan of short horror stories. Assess the pitches on a scale from 1-100, giving preference to those that skillfully combine psychological terror with the authenticity of digital dating experiences. Rate pitches that fail to capture the essence of Tinder dating lower, while those that excel in creating a palpable sense of fear and realism should score higher.

    3. Select the Best Pitch: Identify the pitch that excels in depicting a Tinder dating scenario with genuine horror elements, scoring it based on its realism, psychological impact, and the creativity of its dating horror twist.

    4. Output the Winning Pitch: Showcase the chosen pitch, its score, and the rationale behind its selection. Emphasize its strength in portraying a Tinder dating horror story that is both believable and deeply unsettling, with a unique twist and emotional depth that truly engages and horrifies the audience.

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
    1. Choose Your Narrative Lens: Opt for a first-person narrative to deepen the story's immersive quality.
    2. Develop the Story Pitch: Craft a pitch that encapsulates the essence of a Ouija board encounter, focusing on psychological depth and supernatural aspects.
    3. Inspiration Utilization: Draw from the provided story ideas, blend them, or use original concepts. The goal is to create a pitch that's authentic, engaging, and frightening.
    4. Evaluation Criteria: Judge your pitch based on its portrayal of a Ouija board horror story, its integration of psychological and supernatural elements, and its potential to elicit fear.
    '''
    
    t1_ouija_old = f'''
    **Template for Ouija Board and Occultism Horror Story Creation**

    **Task: Create a Short Horror Story for My YouTube Channel**

    **Pitch Requirements:**

    - **Rooted in Occult Realism:** The story should weave elements of the occult and ouija board mystique into a narrative that feels plausible within its own universe, subtly blending supernatural with the everyday.
    - **Narrative Style:** The story must be told in the first person, giving the impression of a personal encounter with the occult. This approach should make the narrative feel as though it's being recounted from a deeply personal and unsettling memory.
    - **Unique Occult Twist:** Incorporate a distinctive twist related to the occult or ouija board that sets this story apart from typical horror narratives. This twist should be original and enhance the eerie atmosphere.
    - **Complex Characters Involved with the Occult:** Develop characters that are multifaceted and drawn into the world of occultism through their interactions with a ouija board. These characters should drive the story, making their experiences compelling and relatable.
    - **High Emotional and Supernatural Stakes:** Craft a story with significant emotional depth, where the stakes are amplified by the supernatural elements at play. The outcome should deeply affect the reader, making the occult experience resonate on a personal level.


    **Task List:**

    1. **Generate High-Concept Pitches:** Write {no_of_pitches} high-concept pitches for a best-selling horror story that delves into ouija boards and occult themes. Each pitch should feature a unique twist, engaging characters, high emotional stakes, and an unforgettable ending. These pitches should be particularly terrifying, rooted in a first-person narrative as if someone is reliving a haunting memory. Base the pitches on user input ("{user_input}") if provided.
    2. **Critique and Rate Pitches:** Assume the role of both a critic and an avid fan of short horror stories. Evaluate the pitches on a scale from 1-100, prioritizing stories that masterfully blend psychological terror with a touch of realism. Pitches that lack a believable foundation in the occult should receive lower ratings, while those that excel in psychological depth and terror should score higher.
    3. **Select the Best Pitch:** Choose the pitch with the highest rating based on its psychological terror, and how effectively it employs the occult and ouija board elements.
    4. **Output the Winning Pitch:** Present the selected pitch, its rating, and a detailed explanation for its top score. Highlight how it stands out in terms of its realistic approach to the occult, its emotional depth, and its unique, chilling twist.
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

    t1_shifting_reality = '''
    Parallel Universe Horror Story Generation Task
    Objective: Create an intensely scary parallel universe horror story.
    Story Foundation:
    • A gripping hook that reels the listener in
    • Central Theme: An unsettling experience with shifting into a parallel universe. Explore the eerie atmosphere, the dynamics of the new reality, and the protagonist's struggle to understand their situation.
    • Psychological and Supernatural Elements: Combine psychological terror with the consequences of existing in an alternate reality. Characters face fears, unexpected truths, and the aftermath of their actions.
    • First-Person Recollection: Narrate as a personal memory, mimicking the authentic accounts found in Reddit's true horror stories for realism and impact.
    • Climax and Revelation: Include a revelation or twist that changes the narrator’s understanding, such as discovering the parallel universe's dark secrets or realizing they can't return to their original reality.

    Inspiration & Story Ideas in no paricular order:
    - Captured on thee other side: A man wakes up in a paralelle world yhat he really loves. Gets back to his original reality and misses the alternative world  immensely 
    - The Other Side of the Mirror: A man accidentally steps through a mirror and finds himself in a subtly altered version of his home. As he tries to navigate this world, he discovers his doppelgänger plotting to replace him.
    - The Silent Town: A woman wakes up in a town where everything is eerily silent and slightly different. She must uncover the town's secret while avoiding the watchful eyes of its sinister inhabitants.
    - The Looping Day: A teenager group finds themselves reliving the same day, each time with minor and increasingly disturbing changes. They must figure out how to break the loop before it consumes their sanity.
    - The Perfect Stranger: A man meets a seemingly perfect version of his spouse in a parallel universe, only to find out they have a dark and horrifying agenda.
    - The Hidden Corridor: A group of friends discovers a hidden corridor in their school that leads to an alternate version of the building, filled with nightmarish versions of their classmates.
    - The Vanished Family: A woman returns home to find her family replaced by eerily perfect replicas. She must uncover the truth and find a way back to her real family.
    - The Time-Lost Room: A man finds a room in his house that transports him to a different era with subtle but terrifying differences. He must navigate this world and find a way back before he becomes trapped.
    - The Doppelgänger’s Intent: A person keeps encountering their exact double, who seems intent on replacing them. The protagonist must uncover the double's plan and find a way to stop it.
    - The Alien Landscape: A group of friends stumbles into a parallel world with bizarre and dangerous flora and fauna. They must survive and find a way back home.
    - The Whispering Shadows: A teenager finds themselves in a world where shadows seem to whisper and move on their own. They must uncover the shadows' secrets and find a way back to their own reality.

    Task Execution:
    1. Choose Your Narrative Lens: Opt for a first-person narrative to deepen the story's immersive quality.
    2. Develop the Story Pitch: Drawing inspiration from above story ideas - craft a pitch that encapsulates the essence of a parallel universe encounter, focusing on psychological depth and supernatural aspects.
    3. Inspiration Utilization: Draw from the provided story ideas, blend them, or use original concepts. The goal is to create a pitch that's authentic, engaging, and frightening.
    4. Evaluation Criteria: Judge your pitch based on its portrayal of a parallel universe horror story, its integration of psychological and supernatural elements, and its potential to elicit fear.
    '''
    
    match story_type.lower():
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
        case _:
            t1 = t1_occultism

    
  
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
    - Begin with a Compelling Hook: Start your story summary by crafting a powerful opening that immediately grabs the audience's attention. This could be a mysterious event, a chilling revelation, a provocative question, or a foreboding statement that hints at the horror to come. The hook should be closely tied to the core horror element of your story, such as an unsettling encounter with Voodoo magic or a terrifying brush with dark forces, setting the tone for the rest of the narrative.
    - Introduction and Setup: Following the hook, describe the initial setting, introduce the protagonist and key supporting characters, and establish the story’s normal world before the main conflict begins. This part should build on the intrigue created by the hook, drawing the audience deeper into the story’s atmosphere.
    - Beginning, Middle, and End: Detail the progression of the story from the inciting incident through to the climax and resolution. Include how the characters’ relationships evolve, key events that escalate the conflict, settings that enhance the horror, and how the characters confront and ultimately resolve (or fail to resolve) their situation.
    - Character Development Arcs: Explain the protagonist's and key supporting characters’ growth or transformation throughout the story, influenced by their encounters with the supernatural or their journey into the dark aspects of Voodoo and magic.
    - Ensure that each part of your summary maintains the tension and mystery introduced by your opening hook, weaving a cohesive and engaging narrative that keeps the audience listening or reading with bated breath.

    25. Action Beats for Script
    - List {count_action_beats} detailed action beats crucial for the story's development, ensuring the protagonist remains the focal point while integrating up to two supporting characters in these scenes. Each action beat should contribute to building the suspense and horror, echoing the unsettling tone set by your opening hook.
    - For each action beat, provide comprehensive STORY INFORMATION, including setting, character emotions and motivations, and the beat's outcome. Highlight interactions between the protagonist and supporting characters, showcasing their importance to the story and character development.
    '''

    r2 = new_msg(t2)
    print(r2)

    limits = '''NEVER WRITE EDITORIAL STUFF LIKE "action beat" in the story.\n IF something in the story is spelled, make sure to type it with extra spaces and lines after all letters includinig the last letter. It is to make narration slower . example E  -  L  -  I  -  A  -  S  -  " '''
    s1 = new_msg(f'''Now write part 1 of the story covering a compelling hook and intro and actionbeat {beats_split[1]}. Output nothing but part 1 of the story. {limits}''') 
    # print(s1)
    s2 = new_msg(f'''Now write part 2 of the story covering actionbeat {beats_split[2]}. Output nothing but part 2 of the story. {limits}''') 
    # print(s2)
    s3 = new_msg(f'''Now write part 3 of the story covering actionbeat {beats_split[3]} and the ending. Output nothing but part 3 of the story. {limits}''') 
    # print(s3)

    story = s1 + s2 + s3
    count_words(story)

    #save story
    story_no = 1
    path_story = os.path.join(xp_path, fn + " - story " + str(story_no) + ".txt")
    save_file(path_story, story)

    gender = new_msg("What gender is the protagonist? Output only [male/female].")
    print(gender)

    desc = new_msg("Create a good title and a small teaser for this story to be used in a youtube description. Outout only that.")
    path_desc = os.path.join(xp_path, fn + " - desc_ " + str(story_no) + ".txt")
    save_file(path_desc, desc)

    # story = open_file(r"C:\my\__youtube\videos\2024-02-29_1337_True Walmart Horror Stories\Stories - story 1.txt")


    ####################
    # Create images
    ####################
    import tools_create_images as tci

    def create_images():
        image_error_path =r"C:\my\__youtube\videos\Horror Stories - audio_video_defaults\horror_stories_error_default_image.png"
        image_desc = []
        for i in range(1, count_action_beats+1):
        # for i in range(1, 2+1):
            print(i)
            prompt = f'''
                    Use your talents as digital artist to create a detailed image prompt for action beat {i}. 
                    Focusing on visualizing the scene with the protagonist always as the primary focus.
                        - Describe the protagonist and up to two supporting characters involved in the scene making sure to use the generated Character profiles for securing detailed character consistency across images.
                        - Include setting details (time of day, location), important objects, and environmental elements to convey the mood or atmosphere.
                        - Ensure that style of the image is consistent across all the images. Make the images photo realistic, Hasselblad.
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
    def create_thumbnail(user_input = ""):
        path_img = os.path.join(xp_path, fn + " - thumbnail_")
        query = '''Use your talents as digital artist to create a detailed image prompt for a thumbnail to this story on youtube,
                ''' + user_input + '''
                Make sure the prompt complies with OpenAIs policy for image generation. Do not mention any brands.'''
        img_prompt = new_msg(query)
        try:
            image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn= path_img, i=100)
        except:
            try:
                img_prompt = new_msg(f"This prompt was declined by Dall-e. Please rephrase it  carefully: {img_prompt}")
                image_url, filename = tci.chatgpt_dalle(prompt = img_prompt, fn= path_img, i=100)
            except:
                error_list.append("Error in function create_thumbnail()")

    create_thumbnail("")
    # create_thumbnail("Portrait the house the story is happening in")

    ####################
    # Create voice over
    ####################
    import tools_voice_over as tvo
    def create_voice_over(gender):
        path_voice = os.path.join(xp_path, fn + " - " + str(story_no))

        search_term = gender  #"female"
        if search_term.lower()=="female":
            voice = "shimmer"
        else:
            voice = "onyx"
        print(gender, voice)
        tvo.text2mp3(text_string = story, voice_name = voice, fn=path_voice )
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


    ###########################
    # Adding music sound track
    ###########################
    # from add_music_to_mp4 import * 
    # import add_music_to_mp4 as am
    # output_final_mp4_music = os.path.join(xp_path,fn + "final_mp4_w_music.mp4")
    # am.add_ambient_music_to_video(
    #     video_file_path=output_final_mp4,
    #     music_folder_path='C:\\my\\__youtube\\videos\\horror_music',
    #     output_file_path=output_final_mp4_music,
    #     music_volume=0.05  # Adjust volume as needed
    #     )

    return xp_path, error_list
