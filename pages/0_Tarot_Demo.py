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

# Initialize your API key using Streamlit secrets
openai_api_key = st.secrets["openai"]["api_key"]

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

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

# Function to generate a tarot reading
def generate_tarot_reading(tarot_draw, context):
    gpt_model = "gpt-4"
    gpt_temperature = 1
    system_prompt = f"""
    Give me a warm and empathetic 'thesis, antithesis, synthesis' tarot card reading for these cards: {tarot_draw}. When providing the headings for each section, include the card and include the common simple description or name of the card. Interpret how these cards interact in the context of real life challenges and opportunities. Give me a 700 word reading and format this using Markdown formatting.
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
st.title("Thesis Antithesis Synthesis Tarot Reading App")

# User inputs
context = st.text_input("Please provide the context of the reading:", "")

if st.button("Draw Tarot Cards and Generate Reading"):
    # Picking 3 random cards
    # tarot_draw = random.sample(tarot_cards, 3)
    tarot_draw = 'King of Swords, Seven of Cups, Six of Pentacles'

    # Generate tarot reading
    tarot_reading = generate_tarot_reading(tarot_draw, context)

    # Display the results
    st.text(f"Context: {context} ({', '.join(tarot_draw)})")
    st.text(f"Model: GPT-4, Temperature: 1")
    st.subheader("Your Tarot Cards:")
    st.markdown(tarot_reading)
    st.text("========End of Reading========")

