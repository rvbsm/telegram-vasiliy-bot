import asyncio
import logging

from main import bot, dp, db
from aiogram.types import Message, ChatType
from aiogram.utils import exceptions
from aiogram.dispatcher.filters import ChatTypeFilter

log = logging.getLogger('broadcast')

def get_users():
    yield from set(db.getUsers())


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """[summary]

    Args:
        user_id (int): Telegram id of user.
        text (str): Text to be sent.
        disable_notification (bool, optional): Disabling message notification. Defaults to False.

    Returns:
        bool: True on success.
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"[id: {user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"[id: {user_id}]: invalid user id")
    except exceptions.RetryAfter as e:
        log.error(f"[id: {user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text, disable_notification)
    except exceptions.UserDeactivated:
        log.error(f"[id: {user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.error(f"[id: {user_id}]: failed")
    else:
        log.info(f"[id: {user_id}]: success")
        return True
    return False

@dp.message_handler(lambda message: message.from_user.id == 200635302, ChatTypeFilter(ChatType.PRIVATE))
@dp.message_handler(commands="broadcast")
async def broadcaster(message: Message):
    text = message.get_args()
    count = 0
    try:
        for id in get_users():
            if await send_message(id, text, disable_notification=True):
                count += 1
            await asyncio.sleep(.05)
    finally:
        log.info(f"{count} messages successful sent.")

__all__ = ["dp"]