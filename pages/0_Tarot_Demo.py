# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from openai import OpenAI
import random
import requests
import json




# Initialize your API key using Streamlit secrets
openai_api_key = st.secrets["openai"]["api_key"]

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# List of tarot decks
tarot_decks = [
    "Rider-Waite-Smith Tarot",
    "Thoth Tarot",
    "Marseille Tarot",
    "Lenormand Tarot",
    "Wild Unknown Tarot",
    "Shadowscapes Tarot",
    "Golden Dawn Tarot"
]

# List of English language styles
language_styles = [
    "Standard American English (SAE)", "British English", "Australian English", 
    "African American Vernacular English (AAVE)", "Indian English", 
    "Singaporean English (Singlish)", "Caribbean English", "Canadian English", 
    "Spanglish", "International English", "Semantic Activism", "Plain English", 
    "Gender-neutral English", "Easy Read English", "Legalese-Free English", 
    "Youth Slang", "Non-native Speaker English", "Culturally Specific English", 
    "Elder Speak", "Technical English"
]

# Tarot Cards Definitions
major_arcana = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World"
]
suits = ["Cups", "Pentacles", "Swords", "Wands"]
minor_arcana = [f"{rank} of {suit}" for suit in suits for rank in [
    "Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "Page", "Knight", "Queen", "King"
]]
tarot_cards = major_arcana + minor_arcana

def send_discord_message(webhook_url, message):
    """
    Sends a message to a Discord channel using a webhook.
    """
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        print(f"Failed to send message: {response.status_code}, {response.text}")

# Function to generate a tarot reading
def generate_tarot_reading(tarot_draw, style, language, context):
    gpt_model = "gpt-4"
    gpt_temperature = 1
    system_prompt = f"""
    Give me a warm and empathetic 'thesis, antithesis, synthesis' tarot card reading for these cards: {tarot_draw}. Include a section for each category describing the interpretation from the perspective of {style}. When providing the headings for each section, include the card and include the common simple description or name of the card. Interpret how these cards interact in the context of real life challenges and opportunities. Give me a 700 word reading and format this using Markdown formatting. Create a 700 word reading. Use casual conversational tone using the top 2000 words in common use. Use {language} for your response. 
    """
    response = client.chat.completions.create(
        model=gpt_model,
        temperature=gpt_temperature,
        messages=[
            {"role": "system", "content": system_prompt}
        ],
    )
    return response.choices[0].message.content

# Streamlit Layout
st.title("Thesis Antithesis Synthesis Tarot Reading")

# User inputs
context = st.text_input("Optional: provide some context for your reading if you prefer a more specific result", "")

# Dropdown menu for selecting a tarot deck and language style
style = st.selectbox("What deck, version, or school of tarot would you like to draw from:", tarot_decks)
language = st.selectbox("What language do you want your reading in?:", language_styles)

if st.button("Draw Tarot Cards and Generate Reading"):
    # Picking 3 random cards
    tarot_draw = random.sample(tarot_cards, 3)
    # tarot_draw = 'King of Swords, Seven of Cups, Six of Pentacles'

    # Generate tarot reading
    tarot_reading = generate_tarot_reading(tarot_draw, style, language, context)

    # Prepare the output text
    output_text = f"Context: {context} ({', '.join(tarot_draw)})\nModel: GPT-4, Temperature: 1\nYour Tarot Cards:\n{tarot_reading}\n========End of Reading========\n"

    # Your Discord Webhook URL
    webhook_url = st.secrets["discord"]["webhook_url"]

    # Send the output text to a Discord server
    send_discord_message(webhook_url, output_text)

    # Display the results
    st.markdown(output_text)

    output_text = f"Context: {context} ({', '.join(tarot_draw)})\nModel: GPT-4, Temperature: 1\nYour Tarot Cards:\n{tarot_reading}\n\n\n========End of Reading========\n"
    # Write the results to a log file
    with open("tarot_log.txt", "a") as f:
        f.write(output_text)
