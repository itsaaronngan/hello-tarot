import random

tarot_decks = [
    "Rider-Waite-Smith Tarot",
    "Thoth Tarot",
    "Marseille Tarot",
    "Lenormand Tarot",
    "Wild Unknown Tarot",
    "Shadowscapes Tarot",
    "Golden Dawn Tarot"
]

language_styles = [
    "plain english", "Aussie English", 
    "African American Vernacular English (AAVE)", "Indian English", 
    "Singaporean English (Singlish)", "Caribbean English", "Canadian English", 
    "Spanglish", "Semantic Activism", "Gender-neutral English", "Easy Read English", "Shakespearean English",
]

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

tarot_draw_styles = {
    "Thesis Antithesis Synthesis Spread": 3,
    "Three Card Spread (Past, Present, Future)": 3,
    "Celtic Cross Spread": 10,
    "Horseshoe Spread": 7,
    "Five Card Spread": 5,
    "Seven Card Horseshoe Spread": 7,
    "Ten Card Spread": 10,
    "Relationship Spread": 6,
    "Career Spread": 6,
    "Decision Making Spread": 5,
    "Month Ahead Spread": 12,
    "Year Ahead Spread": 12,
    "Daily Draw": 1
    }

def draw_tarot_cards(num_cards=3):
    """
    Draws a specified number of tarot cards from the deck.
    :param num_cards: Number of cards to draw, default is 3
    :return: List of drawn tarot cards
    """
    return random.sample(tarot_cards, num_cards)
