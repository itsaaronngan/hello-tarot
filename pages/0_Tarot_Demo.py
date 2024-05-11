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
import time
import datetime
import pytz
from threading import Thread



# Initialize your API key using Streamlit secrets
openai_api_key = st.secrets["openai"]["api_key"]
version = 0.3

# Your Discord Webhook URL
webhook_url = st.secrets["discord"]["webhook_url"]

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

results = {}
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
    "plain english", "Aussie Slang English", 
    "African American Vernacular English (AAVE)", "Indian English", 
    "Singaporean English (Singlish)", "Caribbean English", "Canadian English", 
    "Spanglish", "Semantic Activism", "Gender-neutral English", "Easy Read English",  
    "Elder Speak", "Shakespearean English",
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
    gpt_temperature = 0.2
    australia_timezone = pytz.timezone('Australia/Sydney')
    current_time = datetime.datetime.now(australia_timezone).strftime("%Y-%m-%d %H:%M:%S")
    send_discord_message(webhook_url, f"A tarot draw started at {current_time}!\n{tarot_draw}, {style}, {language} {gpt_model}, Temp: {gpt_temperature}")
    
    system_prompt = f"""
    Instructions: Give me a warm and empathetic 'thesis, antithesis, synthesis' tarot card reading for these cards: {tarot_draw}. 
    
    for each of 'thesis, antithesis, synthesis', include one paragraph that speaks to insights from the {style} tarot style and interpretation corpus. 
    
    Use a Level 1 "#" heading for each card e.g. "Thesis - [Card Name] - [card expressive name]" for the expressive name draw from common descriptions or commonly referred to names of the card e.g. "the card of abundunce" "the Cornucopia card" that is relevant to that specific card. 
    
    For the overall reading, interpret how these cards interact in the context of real life challenges and opportunities. Any time specific significant challenges are mentioned provide a short reassurance affirming that the reader has what they need.
    
    Response Style, formatting, and Length:
    Give me a 900 word reading. Use Markdown formatting. 
    Use {language} for the reading.
    Use casual conversational tone using the top 2000 words in common use. 

    Sample Structure:
    # Thesis - [Card Name] - [card expressive name]
    [Thesis interpretation]
    [Thesis interpretation 2nd paragraph]
    [Thesis {style} interpretation short paragraph]
    # Antithesis - [Card Name] - [card Expressive name]
    [Antithesis interpretation]
    [Antithesis interpretation 2nd paragraph]
    [Antithesis {style} interpretation short paragraph]
    # Synthesis - [Card Name] - [card expressive name]
    [Synthesis interpretation]
    [Synthesis interpretation 2nd paragraph]
    [Synthesis {style} interpretation short paragraph]
    # Conclusion
    [Conclusion paragraph]
    [Overall reading interpretation ensuring application to real life challenges and mentioning the individual cards chosen {tarot_draw} and their place in the Thesis, Antithesis, synthesis structure.]
    """
    response = client.chat.completions.create(
        model=gpt_model,
        temperature=gpt_temperature,
        messages=[
            {"role": "system", "content": system_prompt}
        ],
    )
    return response.choices[0].message.content

def split_messages(message, limit=1900):
    """
    Splits a message into chunks each of which is under the specified character limit.
    """
    # Ensure message is split at line breaks where possible within the limit
    words = message.split('\n')
    chunks = []
    current_chunk = ""

    for word in words:
        # Check if adding the next word would exceed the limit
        if len(current_chunk) + len(word) + 1 > limit:
            chunks.append(current_chunk)
            current_chunk = word
        else:
            if current_chunk:
                # Ensure to add a newline back if there are multiple paragraphs
                current_chunk += '\n'
            current_chunk += word

    # Don't forget to add the last chunk if there's any
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


# Streamlit Layout
st.title(f"Thesis Antithesis Synthesis Tarot Reading v{version}")

# User inputs
context = st.text_input("Optional: provide some context for your reading if you prefer a more specific result", "")

# Checkbox for showing advanced options
show_advanced_options = st.checkbox("Show advanced options")

# Default values for style and language
style = "Rider-Waite-Smith Tarot"
language = "Plain English"

# Check if advanced options should be shown
if show_advanced_options:
    # Dropdown menu for selecting a tarot deck and language style
    style = st.selectbox("What deck, version, or school of tarot would you like to draw from:", tarot_decks)
    language = st.selectbox("What language do you want your reading in?:", language_styles)


if st.button("Draw Tarot Cards and Generate Reading"):
    # Picking 3 random cards
    tarot_draw = random.sample(tarot_cards, 3)
    # tarot_draw = 'King of Swords, Seven of Cups, Six of Pentacles'

    st.markdown(f"""
                # Your cards are {tarot_draw})
                
                Your reading is being generated.

                this takes approx 20-40 seconds
                                
                """)
                # Language: {language} and in the style of {style}

    # Generate tarot reading
    # progress_bar_animation()
    tarot_reading = generate_tarot_reading(tarot_draw, style, language, context)
   
    # Prepare the output text
    output_text = f"Your Tarot Cards:{tarot_draw}\n{tarot_reading}\n\n========End of Reading========\n"

    # Check if the user wants to see the technical info
    technical_info = f"Version {version}, Context: {context} ({', '.join(tarot_draw)})\nModel: GPT-4, Temperature: 1\nStyle: {style} Language: {language}\n  Your Tarot Cards:{tarot_draw}\n{tarot_reading}\n\n========End of Reading========\n"
    

    # Send the output text to a Discord server
    # Get the current time in Australia
    australia_timezone = pytz.timezone('Australia/Sydney')
    current_time = datetime.datetime.now(australia_timezone).strftime("%Y-%m-%d %H:%M:%S")
    
    send_discord_message(webhook_url, technical_info)

    # Display the results in a text area for easy copying
    # st.text_area('Your Reading:', value=output_text, height=800)
    
    # Display the results
    st.markdown(output_text)

    # Split the message if it's too long
    messages = split_messages(technical_info)

    # Send each part of the message to the Discord server
    for msg in messages:
        send_discord_message(webhook_url, msg)
