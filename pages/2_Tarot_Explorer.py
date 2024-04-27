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

# Replace st.json(cards) with:
if options == "View All Cards":
    for card in cards:
        st.markdown(f"**Name:** {card['name']}\n\n**Suit:** {card['suit']}\n\n**Description:** {card['description']}\n\n---\n")

# Replace st.json(filtered_cards) with:
elif options == "View Cards by Suit":
    for card in filtered_cards:
        st.markdown(f"**Name:** {card['name']}\n\n**Suit:** {card['suit']}\n\n**Description:** {card['description']}\n\n---\n")

# Replace st.json(suits) with:
elif options == "View Suits":
    for suit in suits:
        st.markdown(f"**Name:** {suit['name']}\n\n**Element:** {suit['element']}\n\n**Description:** {suit['description']}\n\n---\n")

# Replace st.json(drawn_cards) with:
elif options == "Draw Cards":
    for card in drawn_cards:
        st.markdown(f"**Name:** {card['name']}\n\n**Suit:** {card['suit']}\n\n**Description:** {card['description']}\n\n---\n")

# Replace st.json(matching_card) with:
elif options == "Find Card by Name":
    if matching_card:
        st.markdown(f"**Name:** {matching_card['name']}\n\n**Suit:** {matching_card['suit']}\n\n**Description:** {matching_card['description']}\n\n---\n")
