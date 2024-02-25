import os, json

script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the emoji keywords
with open(os.path.join(script_dir, 'emoji_keywords.json'), 'r') as f:
    emoji_keywords = json.load(f)

# Load the emojis
with open(os.path.join(script_dir, 'emojis.json'), 'r') as f:
    emojis = json.load(f)

# Merge the data
for category in emojis:
    for emoji in emojis[category]:
        shortcode = emoji.get('shortcode')
        if shortcode in emoji_keywords:
            emoji['keywords'] = emoji_keywords[shortcode]['keywords']

# Save the merged data
with open(os.path.join(script_dir, 'emojis_merged.json'), 'w', encoding='utf-8') as f:
    json.dump(emojis, f, indent=4, ensure_ascii=False)