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
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Simple Tarot! 👋")

    st.sidebar.success("Select Tarot Demo above.")

    st.markdown(
    """
    Welcome to the Thesis-Antithesis-Synthesis Tarot Process!
    **👈 Select a tarot card from the sidebar** to begin each step of the process and discover insights.
    ### Understand the Steps:
    - **Thesis (Tarot Card 1)**: Represents the current situation or issue. [Learn more about Thesis](https://example.com/thesis)
    - **Antithesis (Tarot Card 2)**: Shows the opposing forces or challenges. [Learn more about Antithesis](https://example.com/antithesis)
    - **Synthesis (Tarot Card 3)**: Reveals the resolution or integration of the first two cards. [Learn more about Synthesis](https://example.com/synthesis)
    ### Want to learn more about the tarot process?
    - Check out our [main website](https://example.com)
    - Dive into our [detailed documentation](https://docs.example.com)
    - Ask a question in our [community forums](https://discuss.example.com)
    ### Explore related concepts:
    - Discover how to use tarot for [personal development](https://example.com/personal-development)
    - Learn about the history of tarot in [decision-making processes](https://example.com/history-tarot)
    """
    )


if __name__ == "__main__":
    run()
