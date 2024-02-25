const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

const allEmojis = {};

// Fetch and parse the HTML
axios.get('https://www.webfx.com/tools/emoji-cheat-sheet/').then(response => {
  const html = response.data;
  const $ = cheerio.load(html);

  // Iterate through each emoji category
  $('.section').each((_, section) => {
    const categoryId = $(section).attr('id'); // E.g., "smileys_and_people"
    allEmojis[categoryId] = [];

    // Find all emojis within this category
    $(section).find('._item').each((_, item) => {
      const emojiInfo = {};

      const shortcode = $(item).find('.shortcode').text();
      if (shortcode) {
        emojiInfo.shortcode = shortcode;
      }

      const unicode = $(item).find('.unicode').text();
      if (unicode) {
        emojiInfo.unicode = unicode;
      }

      allEmojis[categoryId].push(emojiInfo);
    });
  });

  console.log(allEmojis);
  fs.writeFileSync('emojis.json', JSON.stringify(allEmojis, null, 4));
}).catch(error => {
  console.log(error);
});
