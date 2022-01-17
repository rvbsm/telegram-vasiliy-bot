from main import bot, dp, db
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import Message, ChatType
from aiogram.utils import exceptions
import re
from fuzzywuzzy import process
from nltk.corpus import stopwords
stopwords = set(stopwords.words(['russian', 'english']))
ban_words = set(open('ban_words.txt', 'r', encoding='utf-8').read().lower().split())


def ban_filter(text: str):
    count = 0
    text = text.lower()
    text = re.sub(r"[^a-zёа-я ]+", '', text)
    cleaned = {word for word in text.split() if word not in stopwords}
    percentage = [process.extractOne(word, ban_words)[1] for word in cleaned]
    count += len([i for i in percentage if i > 93])
    return count


@dp.message_handler(ChatTypeFilter(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]))
async def text_messages(message: Message):
    await db.insertUser(message)
    await db.insertChat(message)

    ban_count = ban_filter(message.text)

    if (ban_count > 0):
        await db.addPoint(message, ban_count)

        title = "<b>Лидеры чата по Е-баллам:</b> \n"
        users = [await db.getUserFromChat(id, message.chat.id) for id in await db.getUsersFromChat(message)]
        users.sort(key=lambda x: x['points'], reverse=True)

        for user in users if users else []:
            try:
                await message.chat.get_member(user['_id'])
                """
                for char in "_*[]()~`>#+-=|{}.!":
                    if char in user['username']:
                        user['username'] = user['username'].replace(char, "\\"+char)
                """
                title += f"@{user['username']} — {user['points']}\n"
            except KeyError:
                """
                for char in "_*[]()~`>#+-=|{}.!":
                    if char in user['first_name']:
                        user['first_name'] = user['first_name'].replace(char, "\\"+char)
                """
                title += f"[{user['first_name']}](tg://user?id={user['_id']}) — user['points']"

            except exceptions.BadRequest:
                pass
        
        try:
            message_id = await db.getTable(message)
            if message_id:    
                result = await bot.edit_message_text(title, message.chat.id, message_id)

        except exceptions.MessageNotModified:
            return
        except exceptions.MessageCantBeEdited:
            return
        except TypeError:
            return

    return

@dp.edited_message_handler(ChatTypeFilter(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP]))
async def edited_text_messages(message: Message):
    await db.insertUser(message)
    await db.insertChat(message)
    
    ban_count = ban_filter(message.text)

    if (ban_count > 0):
        await db.addPoint(message, ban_count)

        title = "<b>Лидеры чата по Е-баллам:</b> \n"
        users = [await db.getUserFromChat(id, message.chat.id) for id in await db.getUsersFromChat(message)]
        users.sort(key=lambda x: x['points'], reverse=True)

        for user in users if users else []:
            try:
                await message.chat.get_member(user['_id'])
                """
                for char in "_*[]()~`>#+-=|{}.!":
                    if char in user['username']:
                        user['username'] = user['username'].replace(char, "\\"+char)
                """
                title += f"@{user['username']} — {user['points']}\n"
            except KeyError:
                """
                for char in "_*[]()~`>#+-=|{}.!":
                    if char in user['first_name']:
                        user['first_name'] = user['first_name'].replace(char, "\\"+char)
                """
                title += f"[{user['first_name']}](tg://user?id={user['_id']}) — user['points']"

            except exceptions.BadRequest:
                pass

        try:
            message_id = await db.getTable(message)
            if message_id:
                result = await bot.edit_message_text(title, message.chat.id, message_id)

        except exceptions.MessageNotModified:
            return
        except exceptions.MessageCantBeEdited:
            return
        except TypeError:
            return

    return
