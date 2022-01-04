from bot import dp, db
from aiogram import types, utils

@dp.message_handler(commands="start")
async def start_message(message: types.Message):
    await db.userInsert(message.from_user)

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text="Разработчик", url="tg://resolve?domain=rvbsm"),
        types.InlineKeyboardButton(text="GitHub", url="https://github.com/rvbsm/")
    )

    return await message.reply("*Кнопачьки:*", reply_markup=markup)

@dp.message_handler(commands="help")
async def help_message(message: types.Message):
    commands = await db.commandsGet()
    commands_text = "*Список доступных комманд:* \n`" + '`\n`'.join(commands) + '`'

    await message.reply(commands_text)


@dp.message_handler(commands="table")
async def table_message(message: types.Message):
    title = "*Лидеры чата по Е\-баллам:* \n"
    users = [await db.userFind(id) for id in await db.usersGet()]
    users.sort(key=lambda x: x['points'], reverse=True)

    for user in users if users else []:
        try:
            await message.chat.get_member(user['_id'])
            
            for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
                    if char in user['username']:
                        user['username'] = user['username'].replace(char, "\\"+char)
            
            title += f"@{user['username']} — {user['points']}\n"
        except KeyError:
            for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
                if char in user['first_name']:
                    user['first_name'] = user['first_name'].replace(char, "\\"+char)
            
            title += f"[{user['first_name']}](tg://user?id={user['_id']}) — user['points']"
        
        except utils.exceptions.BadRequest:
            pass

    result = await message.reply(title)

    try:
        await result.pin(disable_notification=True)
    except utils.exceptions.BadRequest:
        pass

    if (message.chat.type != 'private'):
        chat = message.chat.__dict__["_values"]
        chat['points'] = result.message_id
        await db.userInsert(message.chat)
         

# *bold \*text*
# _italic \*text_
# __underline__
# ~strikethrough~
# ||spoiler||
# *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
# [inline URL](http://www.example.com/)
# [inline mention of a user](tg://user?id=123456789)
# `inline fixed-width code`
# ```
# pre-formatted fixed-width code block
# ```
# ```python
# pre-formatted fixed-width code block written in the Python programming language
# ```
