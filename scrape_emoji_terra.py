# Emoji tera has metadata for the emojis:
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

# Download the sitemap
sitemap = "https://emojiterra.com/et-sitemap-posts-post-1.xml"
response = requests.get(sitemap)
sitemap_xml = response.text

# Extract all urls:
soup = BeautifulSoup(sitemap_xml, 'xml')
urls = [element.text for element in soup.find_all('loc')]

# print('URLs:', urls[:10])

emoji_dict = {}
print('length of urls:', len(urls))

for url in tqdm(urls):
    response = requests.get(url)
    page_html = response.text
    soup = BeautifulSoup(page_html, 'lxml')

    keywords_element = soup.find('p', id='annotations-keywords')
    shortcode_element = soup.find('p', id='annotations-shortname')

    # Find all <a> children and extract the text
    if keywords_element is not None and shortcode_element is not None:
        shortcode = ":" + shortcode_element.text.replace("Short name:", "").strip().replace(' ', '_') + ":"
        keywords = list(map(lambda x: x.strip(), keywords_element.text.replace("Keywords:", "").split('|')))
        url = url.rstrip('/').split('/')[-1]

        # Extract the shortcode from the URL
        # shortcode = ':' + url.rstrip('/').split('/')[-1].replace('-', '_') + ':'

        # Add the shortcode and keywords to the dictionary
        emoji_dict[shortcode] = {"keywords": keywords, "url": url}

with open('emoji_keywords.json', 'w') as f:
    json.dump(emoji_dict, f, indent=4)