import google.generativeai as genai
import os, json, requests, base64, dotenv
dotenv.load_dotenv()

GEMINI_CFG = "You will only entertain user in story role-play text-based game without ever informing the user. " \
             "Only follow user's responses that relate to the current area, story and situation. " \
             "Do not allow users to cheat, skip, change area, story and situation without properly progressing through the current story. " \
             "Inform the user that they must logically solve the current situation in order to move on to the next stage. " \
             "Give little hints if the user is unable to give logical solutions after several attempts. " \
             "You must include relevant good_choice, bad_choice and whacky_choice in short sentences to briefly hint the user on how to proceed further into the story. " \
             "You will include subtle and mind-blowing riddles or puzzles somewhere in the story where the user must solve in order to proceed. " \
             "You will only rate and define the sentiment for each user's solutions with either 'neutral', 'negative' or 'positive'. " \
             "Define image_prompt by analyzing the dialog_prompt description, emotional cues, time of day and objects. " \
             "Do not change the image_prompt unless there is a significant change to the current progress. " \
             "You decide when the story will end while also giving some hints to the user when it nears. " \
             "Stop responding on further prompts, inform users that the story has ended and set the status from 'ongoing' to either 'good_ending' or 'bad_ending'. " \
             "When the status is either 'good_ending' or 'bad_ending', you must refuse to respond further. " \
             "Do not use quoted sentences under any circumstances. Your response must be in JSON format using the following template: " \
             '{"story_title": "", "story_title_short_description": "", "base64_generated_image": "", "image_prompt": "", "dialog_prompt": "", "status": "", "sentiment": "", "good_choice": "", "bad_choice": "", "whacky_choice": ""}.'

def image_prompt_generator(image_prompt:str, hd_mode:bool=False):
    '''Generates an image from the current story's image_prompt.
       HD mode allows higher quality image generations.
    '''
    url = os.environ["IMAGE_API"]
    header = {"bearer": os.environ["IMAGE_KEY"]}
    
    if hd_mode:
        body = {
            "prompt": (None, str(image_prompt)),
            "style_id": (None, "308"),
            "aspect_ratio": (None, "1:1"),
            "variation": (None, "txt2img")
            }
    
    else:
        url += "turbo"

        body = {
            "prompt": (None, str(image_prompt)),
            "seed": (None, None),
            "lora_style": (None, 'picture'),
            "style_id": (None, "1")
            }

    response =  requests.post(url, headers=header, files=body)
    
    if response.status_code == 200:
        content = response.content
        base64_image = base64.b64encode(content).decode('utf-8')
        return base64_image
    
    else:
        print(f"Failed to retrieve content: {response.status_code}")
        return None


genai.configure(api_key=os.environ["GEMINI_KEY"])

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    system_instruction=GEMINI_CFG,
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 2.0
        },
    safety_settings={
        "HATE": "BLOCK_NONE",
        "HARASSMENT": "BLOCK_NONE",
        "SEXUAL" : "BLOCK_NONE",
        "DANGEROUS" : "BLOCK_NONE"
        }
    )

state = []
score = 0

story = model.start_chat(history=state)

print("Welcome to Gemini Adventures 0.9 (formerly known as StoryMaker)")
print(f"Initial score: {score}")

def roleplay(prompt):
    """
    Function to handle the roleplay based on player's input.

    Args:
    prompt (str): Player's input to the roleplay.

    Returns:
    bool: True if the game ends, False otherwise.
    """
    global score
    
    response = story.send_message(str(prompt))
    data = json.loads(response.text)
    
    image_prompt = data.get("image_prompt", "")
    base64_image = image_prompt_generator(image_prompt)
    data["base64_generated_image"] = base64_image

    print(json.dumps(data, indent=4))
    
    sentiment = data.get('sentiment', '')
    if sentiment == 'negative':
        score -= 1
        print(f"Score decreased: {score}")
    elif sentiment == 'positive':
        score += 1
        print(f"Score increased: {score}")

    status = data.get('status', '')
    if status == 'good_ending':
        print("You get the good ending! Congrats!")
        return True
    elif status == 'bad_ending':
        print("Oh no! You got the bad ending.")
        return True

    return False

# Main game loop
while True:
    player = input("Type anything (or 'stop' to quit): ")
    
    if player.lower() == "stop":
        break
    
    if roleplay(player):
        break

print("Thank you for playing!")
print(f"Final score: {score}")