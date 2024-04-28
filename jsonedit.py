import json


with open('tarotjoined.json', 'r') as file:
    tarot_images_data = json.load(file)

# Load the main tarot card data
with open('tarot.json', 'r') as file:
    tarot_main_data = json.load(file)

# Create a dictionary for quick access from tarot_images_data
images_info = {entry["record"]["name"]: entry["record"] for entry in tarot_images_data["data"]}

# Merge the additional information into tarot_main_data
for card in tarot_main_data["cards"]:
    if card["name"] in images_info:
        card_info = images_info[card["name"]]
        card["img"] = card_info.get("img", "")
        card["simplename"] = card_info.get("simplename", "")
        card["altsimplename"] = card_info.get("altsimplename", "")

# Save the updated tarot card data with the additional info
with open('updated_tarot.json', 'w') as file:
    json.dump(tarot_main_data, file, indent=4)

print("Data merged successfully and saved to updated_tarot.json.")