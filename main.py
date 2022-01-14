import config
from database import MongoDB

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

db = MongoDB(config.MONGODB_URI)


__all__ = ["bot", "dp", "db"]
