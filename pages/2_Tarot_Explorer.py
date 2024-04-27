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
import json
import random

# Load tarot data from JSON
def load_tarot_data():
    with open('tarot.json', 'r') as file:
        data = json.load(file)
    return data['cards'], data['suits']

cards, suits = load_tarot_data()

# Streamlit UI
st.title('Tarot Card Explorer')

# Navigation
st.sidebar.title("Navigation")
options = st.sidebar.selectbox("Choose an option", ["View All Cards", "View Cards by Suit", "View Suits", "Draw Cards", "Find Card by Name"])

if options == "View All Cards":
    st.json(cards)

elif options == "View Cards by Suit":
    selected_suit = st.sidebar.selectbox("Select a Suit", [suit['name'] for suit in suits])
    filtered_cards = [card for card in cards if card['suit'].lower() == selected_suit.lower()]
    if filtered_cards:
        st.json(filtered_cards)
    else:
        st.error("No cards found for this suit!")

elif options == "View Suits":
    st.json(suits)

elif options == "Draw Cards":
    n = st.sidebar.number_input("Enter number of cards to draw", min_value=0, value=1)
    if n > 0:
        drawn_cards = random.sample(cards, min(n, len(cards)))
        st.json(drawn_cards)

elif options == "Find Card by Name":
    name_query = st.sidebar.text_input("Enter the card name")
    replacements = {
        "2": "two", "3": "three", "4": "four", "5": "five",
        "6": "six", "7": "seven", "8": "eight", "9": "nine",
        "10": "ten", "1": "ace"
    }
    for digit, word in replacements.items():
        name_query = name_query.replace(digit, word)

    matching_card = next((card for card in cards if card['name'].lower() == name_query.lower()), None)
    if matching_card:
        st.json(matching_card)
    else:
        st.error("Card not found!")
