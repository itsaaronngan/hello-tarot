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

def run():
    st.set_page_config(
        page_title="Helpful Info 👋",
        page_icon="👋",
    )

    st.write("# Welcome to Simple Tarot! 👋")
    st.page_link("pages/0_Tarot_Demo.py", label="Go directly to Tarot Demo", icon="🏠")

    st.sidebar.success("Select Tarot Demo above.")

    st.markdown(
    """
    Welcome to the Thesis-Antithesis-Synthesis Tarot Process!
    **👈 Select a "Tarot Demo" from the sidebar** to begin each step of the process and discover insights.
    ### Understand the Steps:
    - **Thesis (Tarot Card 1)**: Represents the current situation or issue. 
    - **Antithesis (Tarot Card 2)**: Shows the opposing forces or challenges.
    - **Synthesis (Tarot Card 3)**: Reveals the resolution or integration of the first two cards.

    This is a simple tarot reading process that can help you gain insights and clarity on any situation or question.

    This app is under development and will be updated with more features and improvements. Stay tuned for more updates! 🚀

    This app uses GPT-4 from OpenAI to generate tarot card interpretations. 
    """
    )


if __name__ == "__main__":
    run()
