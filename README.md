# 💬 Mindful Escapades
Turn your words into playable adventures! #builtwithgemini

[Watch the promotional video on YouTube](https://www.youtube.com/watch?v=u2PPxwKESUs)

## How Gemini API Empowers This App
Gemini API is a powerful tool that drives a web application designed for creating immersive roleplay text adventures. It transforms user input into engaging narratives, enabling players to embark on limitless storytelling experiences. The API not only generates detailed image prompts for AI-driven visual content but also analyzes player responses to gauge their sentiments. This sentiment analysis plays a crucial role in shaping the narrative, allowing the story to evolve based on player choices and actions.

With Gemini API, players can explore a wide variety of genres and scenarios, from fantasy quests to sci-fi explorations, ensuring that each adventure is unique and tailored to individual preferences. The interactive nature of the platform fosters a dynamic storytelling environment, where players' decisions directly influence the plot's direction and conclusion. As players navigate through the adventures, the API continuously adapts the narrative, creating a personalized experience that keeps them engaged and invested in the story.

Overall, Gemini API enhances the roleplaying experience by seamlessly integrating text generation, image creation and sentiment analysis, making it an invaluable resource for developers looking to create captivating and responsive storytelling applications. The possibilities for adventure are truly endless, limited only by the imagination of the players.

## Setup Guide
- You can always try the online demo hosted on HuggingFace through [here](https://ikmalsaid-mindful-escapades.hf.space/).
- Local installation is supported but you need to provide your own:
  - Gemini API key.
  - Image generation provider URL.
  - Image generation provider API key.
- Once acquired, follow these steps:
  - Clone this repository: `git clone https://github.com/ikmalsaid/mindful-escapades.git`
  - Install the required Python packages: `python -m pip install -r requirements.txt`
  - Create a copy of the `.env.example` file and rename it to `.env`
  - Fill in the required information inside the `.env` file
  - Launch the app using: `python app.py`
  - Wait for the browser window to open.

## How to Use
- Step 1: Type what kind of story that you want in the textbox at the lower part of the app.
- Step 2: Press Enter key or the 'Send' button.
- Step 3: Wait for the response to be shown.
- Step 4: Reply to the response by repeating steps 1 to 3.

## Tips and Release Notes
- You can always change the image style and the type of voice according to your preferences.
- This app operates in Single Session Mode, so only one user should be active at a time to prevent conflicts and issues.
- If you encounter any problems, click the 'Reset All' button to start a new story.
