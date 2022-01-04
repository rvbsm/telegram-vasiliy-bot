import logging
logging.basicConfig(level=logging.INFO)

import bot as main
from bot import bot, dp 
import config
import handlers
from aiogram import executor

def sort_dict():
    old = set(open('ban_words.txt', 'r', encoding='utf-8').read().lower().split())
    new = []
    for word in old:
        if (word not in new and word.isalpha() and len(word) >= 3):
            new.append(word)
        
    new.sort()
    with open('new_ban_words.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(new))


async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)

if __name__ == "__main__":
    # sort_dict()
    if (config.WEBAPP_PORT == 5000):
        executor.start_polling(
            dp,
            skip_updates=True
        )
    executor.start_webhook(
        dp,
        webhook_path=config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT
    )
    # executor.start_polling(dp, skip_updates=True)
