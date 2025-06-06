import io
import requests
import urllib.parse
from google.cloud import vision
from generate_listing import generate_ebay_listing

# === Configuration ===
POKEMON_TCG_API_KEY = "2f5ae158-f224-4652-940a-1e3919611732"  # Replace this
POKEMON_TCG_API_URL = "https://api.pokemontcg.io/v2/cards"
SET_ID = "swsh7"  # Evolving Skies set ID

def extract_text_from_image(image_path):
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ""

def search_card_in_tcg_api(text):
    import re
    headers = {"X-Api-Key": POKEMON_TCG_API_KEY}

    lines = text.split('\n')
    card_number = None
    card_name = None

    # Extract set number (e.g. 215/203 ➝ 215)
    for line in lines:
        match = re.search(r'(\d+)/\d+', line)
        if match:
            card_number = match.group(1)

    # Normalize name for known hits (customizable later)
    for line in lines:
        if "Umbreon" in line and ("V" in line or "VMAX" in line):
            card_name = "Umbreon VMAX"
            break

    if card_number:
        query = f'set.id:{SET_ID} number:{card_number}'
    elif card_name:
        query = f'name:"{card_name}"'
    else:
        query = text

    encoded_query = urllib.parse.quote(query)
    url = f"{POKEMON_TCG_API_URL}?q={encoded_query}"

    print(f"🔵 Querying TCG API with: {query}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200 and response.json()["data"]:
        return response.json()["data"][0]
    return None

def get_card_market_price(card):
    if "cardmarket" in card and "prices" in card["cardmarket"]:
        return card["cardmarket"]["prices"].get("averageSellPrice")
    return None

def identify_card(image_path):
    text = extract_text_from_image(image_path)
    print(f"🕵️ OCR Text:\n{text}")

    card = search_card_in_tcg_api(text)
    if not card:
        print("❌ Card not found.")
        return None

    price = get_card_market_price(card)
    return {
        "name": card["name"],
        "set": card["set"]["name"],
        "number": card["number"],
        "rarity": card.get("rarity", "Unknown"),
        "market_price": price,
        "image_url": card["images"]["large"]
    }

# === Run ===
if __name__ == "__main__":
    image_path = "C:/Users/marke/Documents/program/umbreeion.jpg"  # Replace with your image
    result = identify_card(image_path)
    if result:
        listing = generate_ebay_listing(result)
        print("\n📌 EBAY TITLE:\n" + listing["title"])
        print("\n📝 EBAY DESCRIPTION:\n" + listing["description"])
        print("\n✅ CARD FOUND:")
        print(f"Name: {result['name']}")
        print(f"Set: {result['set']}")
        print(f"Number: {result['number']}")
        print(f"Rarity: {result['rarity']}")
        print(f"Market Price: ${result['market_price']}")
        print(f"Image URL: {result['image_url']}")
