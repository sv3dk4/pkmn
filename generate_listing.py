def generate_ebay_listing(card):
    name = card['name']
    set_name = card['set']
    number = card['number']
    rarity = card['rarity']
    price = card['market_price']
    
    title = f"{name} {set_name} {number} Holo {rarity} Pokémon TCG Card NM - Vaulted Rare 🔥"

    description = f"""
✨ {name} from the {set_name} set!
Card #{number} • Rarity: {rarity}
Condition: Near Mint - straight from a pack, stored with care.

🛡️ Guaranteed Authentic
⚡ Shipped same or next business day in a penny sleeve + toploader
💵 Market Value: ${price:.2f} — Starting at just 99¢!

📦 Ships via eBay Standard Envelope with tracking for fast & safe delivery.

Don't miss out on this iconic collectible! 🐾
    """.strip()

    return {
        "title": title,
        "description": description
    }

# === Test Example ===
if __name__ == "__main__":
    example_card = {
        "name": "Umbreon VMAX",
        "set": "Evolving Skies",
        "number": "215",
        "rarity": "Rare Rainbow",
        "market_price": 1515.39
    }

    listing = generate_ebay_listing(example_card)
    print("\n📌 TITLE:\n" + listing["title"])
    print("\n📝 DESCRIPTION:\n" + listing["description"])
