from bot import bot, dp, db
from aiogram import types, utils
from fuzzywuzzy import process
import re

ban_words = set(open('ban_words.txt', 'r', encoding='utf-8').read().lower().split())

def ban_filter(text: str):
    count = 0
    text = set(re.sub(r"[^a-zA-ZЁёА-я]+", ' ', text).lower().split())

    for word in text:
        if (process.extractOne(word, ban_words)[1] > 95):
            count += 1

    return count, len(text)


@dp.message_handler()
async def text_messages(message: types.Message):
    await db.userInsert(message.from_user)

    ban_count, total_count = ban_filter(message.text)

    if (ban_count > 0):
        await db.addPoint(message.from_user, ban_count)

        title = "*Лидеры чата по Е\-баллам:* \n"
        users = [await db.userFind(id) for id in await db.usersGet()]
        users.sort(key=lambda x: x['points'], reverse=True)

        for user in users if users else []:
            try:
                await message.chat.get_member(user['_id'])
                
                for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
                    if char in user['username']:
                        user['username'] = user['username'].replace(char, "\\"+char)
                
                title += f"@{user['username']} — {user['points']}"
            except KeyError:
                for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
                    if char in user['first_name']:
                        user['first_name'] = user['first_name'].replace(char, "\\"+char)
                
                title += f"[{user['first_name']}](tg://user?id={user['_id']}) — user['points']"
            
            except utils.exceptions.BadRequest:
                pass
        
        message_id = (await db.userFind(message.chat.id))['points']
        try:
            result = await bot.edit_message_text(title, message.chat.id, message_id)
        except utils.exceptions.MessageNotModified:
            return
        except utils.exceptions.MessageCantBeEdited:
            return

    return

@dp.edited_message_handler()
async def edited_text_messages(message: types.Message):
    await db.userInsert(message.from_user)
    
    ban_count, total_count = ban_filter(message.text)

    if (ban_count > 0):
        await db.addPoint(message.from_user, ban_count)

        title = "*Лидеры чата по Е\-баллам:* \n"
        users = [await db.userFind(id) for id in await db.usersGet()]
        users.sort(key=lambda x: x['points'], reverse=True)

        for user in users if users else []:
            try:
                await message.chat.get_member(user['_id'])

                for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
                    if char in user['username']:
                        user['username'] = user['username'].replace(char, "\\"+char)

                title += f"@{user['username']} — {user['points']}"
            except KeyError:
                for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
                    if char in user['first_name']:
                        user['first_name'] = user['first_name'].replace(char, "\\"+char)
                
                title += f"[{user['first_name']}](tg://user?id={user['_id']}) — user['points']"
            
            except utils.exceptions.BadRequest:
                pass
        
        message_id = (await db.userFind(message.chat.id))['points']
        try:
            result = await bot.edit_message_text(title, message.chat.id, message_id)
        except utils.exceptions.MessageNotModified:
            return
        except utils.exceptions.MessageCantBeEdited:
            return

    return
