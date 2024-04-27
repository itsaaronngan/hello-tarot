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

# Load the data
with open('tarot.json') as f:
    data = json.load(f)
    cards = data['cards']
    suits = data['suits']

# Function to get card by suit and rank
def get_card_by_suit_and_rank(suit, rank):
    for card in cards:
        if card['suit'].lower() == suit.lower() and str(card['rank']).lower() == rank.lower():
            return card
    return None

# Function to get all cards of a suit
def get_cards_by_suit(suit):
    return [card for card in cards if card['suit'].lower() == suit.lower()]

# Function to draw n cards
def draw_cards(n):
    return random.sample(cards, n)

# Function to find card by name
def find_card_by_name(name):
    for card in cards:
        if card['name'].lower() == name.lower():
            return card
    return None

def format_card(card):
    description = f"**Planet:** {card['planet']}, **Element:** {card['element']}\n\n**Upright Meanings:** {', '.join(card['meanings']['upright'])}\n\n**Reversed Meanings:** {', '.join(card['meanings']['reversed'])}"
    return f"**Name:** {card['name']}\n\n**Suit:** {card['suit']}\n\n{description}\n\n---\n"

# Streamlit UI
st.set_page_config(
        page_title="Card Explorer",
        page_icon="👋",
    )
st.title('Tarot Card Explorer')

# Navigation
st.sidebar.title("Navigation")
options = st.sidebar.selectbox("Choose an option", ["View All Cards", "View Cards by Suit", "View Suits", "Draw Cards", "Find Card by Name"])

if options == "View All Cards":
    for card in cards:
        st.markdown(format_card(card))

elif options == "View Cards by Suit":
    selected_suit = st.sidebar.selectbox("Select a Suit", [suit['name'] for suit in suits])
    filtered_cards = [card for card in cards if card['suit'].lower() == selected_suit.lower()]
    if filtered_cards:
        for card in filtered_cards:
            st.markdown(format_card(card))
    else:
        st.error("No cards found for this suit!")

elif options == "View Suits":
    st.json(suits)

elif options == "Draw Cards":
    n = st.sidebar.number_input("Enter number of cards to draw", min_value=0, value=1)
    if n > 0:
        drawn_cards = random.sample(cards, min(n, len(cards)))
        for card in drawn_cards:
            st.markdown(format_card(card))

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
        st.markdown(format_card(matching_card))
    else:
        st.error("Card not found!")

