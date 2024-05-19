import streamlit as st
import os

def run():
    st.set_page_config(
        page_title="Simple Tarot",
        page_icon="🔮",
    )

    st.write("# Welcome to Simple Tarot! 🔮")
    st.markdown(
        """
        Welcome to Simple Tarot, dear friend. 🌟

        **We’re here to help you find clarity and peace through the wisdom of tarot.**

        ### How It Works:
        1. **Add your personal context** (if you like, this is optional).
        2. **Click generate reading** and let us gently guide you through a simple Thesis, Antithesis, Synthesis reading.
        """
    )

    st.page_link("pages/0_Simple_Tarot.py", label="🔮🔮🔮 Begin your reading now 🔮🔮🔮", icon="🙏")
    
    st.markdown("---", unsafe_allow_html=True)

    st.markdown(
        """
        ### The Thesis, Antithesis, Synthesis Method:
        - **Thesis (Card 1)**: Reflects your current situation, helping you understand where you are.
        - **Antithesis (Card 2)**: Highlights challenges or opposing forces you may be facing.
        - **Synthesis (Card 3)**: Offers a resolution or integration, showing the path forward.

        Begin your journey by selecting **"Simple Tarot"** from the sidebar. Let us help you navigate life's uncertainties with compassion and insight.
        """
    )

    st.page_link("pages/0_Simple_Tarot.py", label="🔮🔮🔮 Begin your reading now 🔮🔮🔮", icon="🙏")

    st.markdown("---", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        This app uses GPT-4 from OpenAI to provide thoughtful and empathetic interpretations of your tarot cards.

        We hope you find comfort and guidance in your tarot journey. You are not alone. 💖
        """
    )

    st.page_link("pages/0_Simple_Tarot.py", label="🔮🔮🔮 Begin your reading now 🔮🔮🔮", icon="🙏")

    if st.button("Learn About Advanced Options"):
        st.markdown(
            """
            ### Advanced Options:

            For those who seek a more tailored experience, our advanced options offer:

            - **Select a specific tarot deck**: Choose from a variety of decks to find the imagery that resonates with you.
            - **Pick a language style**: Receive your reading in different English dialects or styles, from plain English to Shakespearean English.
            - **Choose a tarot draw style**: Explore various spreads like the Celtic Cross, Horseshoe Spread, or Career Spread to suit your needs.

            Advanced options provide a deeper, more personalized reading experience. 

            Stay tuned for more features and updates 🙏
            """
        )

    st.sidebar.success("Select Simple Tarot to begin your reading.")

if __name__ == "__main__":
    run()
