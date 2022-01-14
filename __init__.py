import nltk
nltk.download('stopwords')

import config
import main
from main import bot, dp
import handlers

from aiogram.utils.executor import start_polling, start_webhook
from fuzzywuzzy import process


async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)

def sort_dict():
    old = set(open('ban_words.txt', 'r', encoding='utf-8').read().lower().split())
    new = ['блять']

    for word in old:
        perc = process.extractOne(word, new)[1]
        if (word not in new and perc <= 93 and len(word) >= 3):
            new.append(word)
        
    new.sort()
    with open('new_ban_words.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(new))

if __name__ == "__main__":
    if (config.WEBAPP_PORT == 5000):
        start_polling(
            dp,
            skip_updates=True
        )
        # sort_dict()
    
    
    else:
        start_webhook(
            dp,
            webhook_path=config.WEBHOOK_PATH,
            skip_updates=True,
            on_startup=on_startup,
            host=config.WEBAPP_HOST,
            port=config.WEBAPP_PORT
        )
