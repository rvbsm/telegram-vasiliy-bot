import config
from database import MongoDB
from aiogram import Bot, Dispatcher

bot = Bot(token=config.BOT_TOKEN, parse_mode="MarkdownV2")
dp = Dispatcher(bot)
db = MongoDB(config.MONGODB_URI)
