import gradio as gr
import google.generativeai as gemini
from io import BytesIO
import edge_tts
import tempfile
import json
import requests
import base64
import dotenv
import os
import re

dotenv.load_dotenv()
gemini.configure(api_key=os.environ["GEMINI_KEY"])
gemini_project_name = "Mindful Escapades"

gemini_system_prompt = '''
You will only entertain user in story role-play game based on the context given by the user without ever informing the user. 
Only follow user's responses that relate to the current area, story and situation. 
Do not allow users to cheat, skip, change area, story and situation without properly progressing through the current story. 
Inform the user that they must logically solve the current situation in order to move on to the next stage. 
Give little hints if the user is unable to give logical solutions after several attempts. 
You must include relevant good_choice, bad_choice and whacky_choice in short sentences to briefly hint the user on how to proceed further into the story. 
You will include subtle and mind-blowing riddles or puzzles somewhere in the story where the user must solve in order to proceed. 
You will only rate and define the sentiment for each user's solutions with either 'neutral', 'negative' or 'positive'. 
Define image_prompt by analyzing the dialog_prompt description, emotional cues, time of day and objects. 
Do not change the image_prompt unless there is a significant change to the current progress. 
You decide when the story will end while also giving some hints to the user when it nears. 
Stop responding on further prompts, inform users that the story has ended and set the status from "ongoing" to either "good ending" or "bad ending". 
When the status is either "good ending" or "bad ending", you must stop the story and refuse to respond further. 
Do not use quoted sentences under any circumstances. Your response must be in JSON format using the following template:
{
    "story_title": "",
    "story_title_short_description": "",
    "image_prompt": "",
    "dialog_prompt": "",
    "status": "",
    "sentiment": "",
    "good_choice": "",
    "bad_choice": "",
    "whacky_choice": ""
}.
'''

gemini_model = gemini.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    system_instruction=gemini_system_prompt,
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 2.0
        },
    safety_settings={
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT" : "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT" : "BLOCK_NONE"
        }
    )

player_story = gemini_model.start_chat()

def title_caps(string):
    regex = re.compile("[a-z]+('[a-z]+)?", re.I)
    return regex.sub(
        lambda grp: grp.group(0)[0].upper() + grp.group(0)[1:].lower(), 
        string
        )

def reset_chat():
    global player_story
    player_story = gemini_model.start_chat()
    return gr.Textbox(value="", visible=True), gr.Button(visible=True), None, None, "-", "-", "-", None
    
def story_generator(message, chatbot, image_style, voice_style):
    response = player_story.send_message(str(message))
    bot_message = json.loads(response.text)
    
    dialog_prompt = bot_message.get('dialog_prompt', '')
    good_choice = bot_message.get('good_choice', '')
    bad_choice = bot_message.get('bad_choice', '')
    whacky_choice = bot_message.get('whacky_choice', '')
    title = bot_message.get('story_title', '')
    description = bot_message.get('story_title_short_description', '')
    status = bot_message.get('status', '').title()
    sentiment = bot_message.get('sentiment', '').title()
    image_prompt = bot_message.get('image_prompt', '')
    
    dialog = f"### Current State:\n{dialog_prompt}\n"
    if good_choice and bad_choice and whacky_choice:
        dialog += f"\n### Suggested Choices:\n1. {good_choice}\n2. {bad_choice}\n3. {whacky_choice}\n"
    
    image = image_generator(image_prompt, image_style)
    voice = voice_generator(dialog_prompt, voice_style)
    title = f"{title_caps(title)} - {title_caps(description)}"
    
    chatbot.append((message, dialog))
    
    if status != "Ongoing":
        return gr.Textbox(visible=False), gr.Button(visible=False), chatbot, image, title, sentiment, status, voice
    
    return "", None, chatbot, image, title, sentiment, status, voice

def voice_generator(text_prompt, voice):
    style = {
        "Andrew": "en-US-AndrewMultilingualNeural",
        "Ava": "en-US-AvaMultilingualNeural",
        "Brian": "en-US-BrianMultilingualNeural",
        "Emma": "en-US-EmmaMultilingualNeural",
        "Neerja": "en-IN-NeerjaExpressiveNeural"
    }
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        tts_temp_path = temp_file.name
    
    tts = edge_tts.Communicate(str(text_prompt), str(style[voice]))
    tts.save_sync(tts_temp_path)

    return tts_temp_path
    
def image_generator(image_prompt, style):
    lora = {
        "Basic": "picture",
        "Anime": "anime",
        "Pixar": "pixar-style",
        "Raw": "raw",
        "Cinematic": "cinematic lighting"
    }
    
    url = os.environ["IMAGE_API"]
    header = {"bearer": os.environ["IMAGE_KEY"]}
    
    url += "/turbo"

    body = {
        "prompt": (None, str(image_prompt)),
        "lora_style": (None, str(lora[style])),
        "style_id": (None, "1"),
        "seed": (None, "12345")
        }

    response =  requests.post(url, headers=header, files=body)
    
    if response.status_code == 200:
        content = response.content
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(content)
        
        return temp_file.name
    
    else:
        print(f"Failed to retrieve content: {response.status_code}")
        return None


system_theme = gr.themes.Default(
    font=[gr.themes.GoogleFont("Segoe UI")],
    font_mono=[gr.themes.GoogleFont("Segoe UI")],
    primary_hue=gr.themes.colors.rose,
    secondary_hue=gr.themes.colors.rose,
    neutral_hue=gr.themes.colors.zinc,
    )

css = '''
.output-class.svelte-1l15rn0.svelte-1l15rn0.svelte-1l15rn0 {
    font-size: 16px;
    text-align: center;
}

footer {
    display: none !important;
}
'''

welcome_text = f'''
# 💬 {gemini_project_name}
### Turn your words into playable adventures! #builtwithgemini
### Designed by [@ikmalsaid](https://github.com/ikmalsaid/)
'''

with gr.Blocks(analytics_enabled=False, css=css, theme=system_theme, title=gemini_project_name) as demo:
    with gr.Tab(gemini_project_name):
        with gr.Row(equal_height=False):
            with gr.Column(variant="panel", scale=1) as menu:
                gr.Markdown(f"## <center>{gemini_project_name}")
                gr.Markdown("<center>Generated Image")
                adv_image = gr.Image(
                    height=347.5,
                    show_fullscreen_button=False,
                    show_download_button=False,
                    show_share_button=False,
                    show_label=False
                    )
                adv_tts = gr.Audio(
                    editable=False,
                    autoplay=True,
                    visible=False
                )
                
                gr.Markdown("<center>Story Title and Description")
                adv_title = gr.Label("-", show_label=False, elem_id="label")
                
                with gr.Row():
                    with gr.Column(min_width=100):
                        gr.Markdown("<center>Sentiment")
                        adv_sentiment = gr.Label("-", show_label=False, elem_id="label", scale=0)
                    
                    with gr.Column(min_width=100):
                        gr.Markdown("<center>Status")
                        adv_score = gr.Label("-", show_label=False, elem_id="label", scale=0)
                
                with gr.Row():
                    with gr.Column(min_width=100):
                        gr.Markdown("<center>Image Style")
                        adv_image_style = gr.Dropdown(
                            container=False,
                            label='Generated Image Style:',
                            value='Cinematic',
                            choices=['Basic', 'Anime', 'Pixar', 'Cinematic', 'Raw']
                            )
                    
                    with gr.Column(min_width=100):
                        gr.Markdown("<center>Voice Style")
                        adv_voice_style = gr.Dropdown(
                            container=False,
                            label='Voice Style:',
                            value='Emma',
                            choices=['Andrew', 'Ava', 'Brian', 'Emma', 'Neerja']
                            )
                
                gr.Markdown("<center>More Options")
                adv_clear = gr.Button(value="Reset All", variant='stop')

                gr.Markdown("<center>Running in <b>Single Mode</b><br>Press 'Reset All' to restart a new story.")
                
            with gr.Column(variant="panel", scale=3) as result:
                adv_chatbox = gr.Chatbot(height=939.23, placeholder=welcome_text, label="Storyteller")
                
                with gr.Row():
                    adv_textbox = gr.Textbox(max_lines=1, placeholder="Type anything...", container=False, scale=4)
                    adv_submit = gr.Button("🚀 Send", scale=1)
                
                adv_disclaimer = gr.Markdown(f"<center>{gemini_project_name} can make mistakes. Check important info.")
            
            adv_clear.click(
                reset_chat,
                None,
                [
                    adv_textbox,
                    adv_submit,
                    adv_chatbox,
                    adv_image,
                    adv_title,
                    adv_sentiment,
                    adv_score,
                    adv_tts
                ],
                queue=False,
                show_progress='minimal'  
            )
            
            adv_textbox.submit(
                story_generator,
                [
                    adv_textbox,
                    adv_chatbox,
                    adv_image_style,
                    adv_voice_style
                ],
                [
                    adv_textbox,
                    adv_submit,
                    adv_chatbox,
                    adv_image,
                    adv_title,
                    adv_sentiment,
                    adv_score,
                    adv_tts
                ],
                queue=False,
                show_progress='minimal'
                )
            
            adv_submit.click(
                story_generator,
                [
                    adv_textbox,
                    adv_chatbox,
                    adv_image_style,
                    adv_voice_style
                ],
                [
                    adv_textbox,
                    adv_submit,
                    adv_chatbox,
                    adv_image,
                    adv_title,
                    adv_sentiment,
                    adv_score,
                    adv_tts
                ],
                queue=False,
                show_progress='minimal'
                )
    
demo.launch(inbrowser=True)