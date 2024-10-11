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
from tarot_config import tarot_decks, language_styles, draw_tarot_cards, tarot_draw_styles


# Initialize your API key using Streamlit secrets
openai_api_key = st.secrets["openai"]["api_key"]
version = 0.6

# Your Discord Webhook URL
webhook_url = st.secrets["discord"]["webhook_url"]

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

results = {}
# List of tarot decks
# tarot_decks = [
#     "Rider-Waite-Smith Tarot",
#     "Thoth Tarot",
#     "Marseille Tarot",
#     "Lenormand Tarot",
#     "Wild Unknown Tarot",
#     "Shadowscapes Tarot",
#     "Golden Dawn Tarot"
# ]

# List of English language styles
# language_styles = [
#     "plain english", "Aussie Slang English", 
#     "African American Vernacular English (AAVE)", "Indian English", 
#     "Singaporean English (Singlish)", "Caribbean English", "Canadian English", 
#     "Spanglish", "Semantic Activism", "Gender-neutral English", "Easy Read English",  
#     "Elder Speak", "Shakespearean English",
# ]

# Tarot Cards Definitions
# major_arcana = [
#     "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
#     "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
#     "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
#     "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
#     "Judgement", "The World"
# ]
# suits = ["Cups", "Pentacles", "Swords", "Wands"]
# minor_arcana = [f"{rank} of {suit}" for suit in suits for rank in [
#     "Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
#     "Page", "Knight", "Queen", "King"
# ]]
# tarot_cards = major_arcana + minor_arcana

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
def generate_tarot_reading(tarot_draw, deck, language, context, draw_style, num_cards):
    australia_timezone = pytz.timezone('Australia/Sydney')
    current_time = datetime.datetime.now(australia_timezone).strftime("%Y-%m-%d %H:%M:%S")
    send_discord_message(webhook_url, f"A tarot draw started at {current_time}!\n {draw_style} \n{tarot_draw}, {deck}, {language} {gpt_model}, Temp: {gpt_temperature}")
    
    wordcount = 200 * num_cards
    context_string = f"Reference my provided reading context: {context}" if context else ""
    context_describe_string = f"""integrate this reading context. Be sensitive to the emotions/potential reactivity of the user. inform gently that context is considered with great care. Context: {context}.  
    """ if context else ""
    style_string = f"Consider the classical tarot deck for this reading: {deck}" if deck else ""
    language_string = f"important, for the entire output make sure this is worded and toned using {language}" if language else ""
    instruction_string = f"Instructions: Give me a warm and empathetic {draw_style} tarot reading based on these cards: {tarot_draw}. "
     
    
    system_prompt = f"""
    {instruction_string}
    {context_string}
    {style_string}
    
    ## Instructions
    Create the reading with a total of {wordcount} words. Follow the sample structure exactly. {language_string}. Use casual conversational gentle tone. 

    ## Tone, Style, and Language
    Avoid white juju and overly positive language that is overly vague/shallow. Avoid self-help buzzwords. Instead of using words like "transformation" use "transmutation", instead of "manifest" make references to "taking action" Use a gentle, empathetic, and respectful tone. Avoid overly formal language. If appropriate, reference the complexity inherant in life: e.g. happiness cannot be appreciated without sorrow.

    ## Sample Structure:
    ### [{draw_style}] Reading
    [gentle 70 word introduction explaining the basics of {draw_style} and the purpose of the reading. {context_describe_string}. tone: respectful, warm, gentle, empathetic. avoid: greetings such as "hi there" or "hello there", excitement, overenthusiasm, chipper.]

    # Your Reading [short simple expressive title based on reading and context if available]
    ## [Section Title based on spread style] - [Card Name] - [card expressive name]
    [Para 1]
    [Para 2]
    [Para 3]
    ## [Section Title based on spread style] - [Card Name] - [card expressive name]
    [Para 1]
    [Para 2]
    [Para 3]

    (continue for total sections)
 
    # Conclusion
    [Conclusion Paragraph - Overall reading interpretation ensuring application to Context ({context}). Mentioning tarot draw: {tarot_draw} and their interpretation in the {draw_style}.]
    [brief comment on the reading from the perspective of {deck} tarot deck and interpretation corpus.]

    {language_string}
    """
    response = client.chat.completions.create(
        model=gpt_model,
        temperature=gpt_temperature,
        messages=[
            {"role": "system", "content": system_prompt}
        ],
    )
    return response.choices[0].message.content

# Callback function to update the draw style
def update_draw_style():
    st.session_state.draw_style = st.session_state.selected_draw_style
    st.session_state.num_cards = tarot_draw_styles[st.session_state.selected_draw_style]


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
deck = ""
language = ""
draw_style = "Thesis Antithesis Synthesis Spread"

if 'draw_style' not in st.session_state:
    st.session_state.draw_style = draw_style

st.title(f"Simple Tarot Reading🔮")
st.subheader(f"{draw_style} v{version}")

# User inputs
context = st.text_input("Optional attunement: Align this reading with your personal situation, context or emotions", "")
num_cards = 3

# Checkbox for showing advanced options
show_advanced_options = st.checkbox("Show advanced options")
st.markdown("Engage with more in-depth readings via an interactive ChatGPT conversation enabled Telegram bot.")
st.markdown("[🔮Telegram Tarot Bot - @threecardgpttarot_bot 🔮](https://t.me/threecardtgpttarot_bot)")

# Default values for deck and language

override_cards = ""

# Check if advanced options should be shown
if show_advanced_options:
    # Dropdown menu for selecting a tarot deck and language style
    deck = st.selectbox("What deck, version, or school of tarot would you like to draw from:", [''] + tarot_decks)
    language = st.selectbox("What language do you want your reading in?:", [''] + language_styles)
    draw_style = st.selectbox("Select a tarot draw style:", list(tarot_draw_styles.keys()), key='selected_draw_style', on_change=update_draw_style)
    num_cards = tarot_draw_styles[draw_style]
        # Text input for overriding the drawn cards
    override_cards = st.text_input("Input your own card draw")

if st.button("Generate Reading" if override_cards else "Draw Tarot Cards and Generate Reading"):
    # Check if the user has provided overridden cards
    if override_cards:
        tarot_draw = override_cards
    else:
        if draw_style in tarot_draw_styles:
            num_cards = tarot_draw_styles[draw_style]
        else:
            num_cards = 3
        tarot_draw = draw_tarot_cards(num_cards)

    # tarot_draw = 'King of Swords, Seven of Cups, Six of Pentacles'

    st.markdown(f"""
                # Generating {draw_style} 
                ### Cards: {tarot_draw}
                Your reading is being generated and will take 10-20 seconds.
                Context: {context}                
                Note: Readings are now available via telegram bot allowing a more in depth (ChatGPT supported conversation) that can support you in engaging with your reading. https://t.me/threecardtgpttarot_bot
                """)
                # Language: {language} and in the style of {style}
    gpt_model = "gpt-4o"
    gpt_temperature = 0.2
    # Generate tarot reading

    
    tarot_reading = generate_tarot_reading(tarot_draw, deck, language, context, draw_style, num_cards)
   
    # Prepare the output text
    output_text = f"Your Tarot Cards:{tarot_draw}, Draw Style: {draw_style} \n{tarot_reading}\n\n========End of Reading========\n"

    # Check if the user wants to see the technical info
    technical_info = f"Version {version}, Draw Style: {draw_style}. Context: {context} ({', '.join(tarot_draw)})\nModel: {gpt_model} Temperature: {gpt_temperature} \nStyle: {deck} Language: {language}\n  Your Tarot Cards:{tarot_draw}\n{tarot_reading}\n\n========End of Reading========\n Note: Readings are now available via telegram bot allowing a more in depth (ChatGPT supported conversation) that can support you in engaging with your reading. https://t.me/threecardtgpttarot_bot"
    

    # Send the output text to a Discord server
    # Get the current time in Australia
    australia_timezone = pytz.timezone('Australia/Sydney')
    current_time = datetime.datetime.now(australia_timezone).strftime("%Y-%m-%d %H:%M:%S")
    
    # Display the results in a text area for easy copying
    # st.text_area('Your Reading:', value=output_text, height=800)
    
    # Display the results
    st.markdown(output_text)

    st.download_button(
        label="Download .txt file Reading",
        data=output_text,
        file_name="tarot_reading.txt",
        mime="text/plain",
    )

    # Split the message if it's too long
    messages = split_messages(technical_info)

    # Send each part of the message to the Discord server
    for msg in messages:
        send_discord_message(webhook_url, msg)
