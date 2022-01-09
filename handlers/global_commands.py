from main import dp, db, bot
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter
from aiogram.types import Message, ChatType, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions


@dp.message_handler(CommandStart(), commands="start")
async def start_message(message: Message):
    await db.insertUser(message)
    bot_me = await bot.get_me()
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(InlineKeyboardButton(text="Добавить меня в чат", url="tg://resolve?domain={0}&startgroup".format(bot_me.username)))
    markup.add(
        InlineKeyboardButton(text="Разработчик", url="tg://resolve?domain=rvbsm"),
        InlineKeyboardButton(text="GitHub", url="https://github.com/rvbsm/")
    )

    await message.reply("*Кнопачьки:*", reply_markup=markup)

@dp.message_handler(commands="help")
async def help_message(message: Message):
    commands = await db.getCommands(message)
    commands_text = "*Список доступных комманд:* \n`" + '`\n`'.join(commands) + '`'

    await message.reply(commands_text)


@dp.message_handler(ChatTypeFilter(chat_type=[ChatType.GROUP, ChatType.SUPER_GROUP]))
@dp.message_handler(commands="table")
async def table_message(message: Message):
    title = "*Лидеры чата по Е\-баллам:* \n"
    users = [await db.getUserFromChat(id, message.chat.id) for id in await db.getUsersFromChat(message)]
    users.sort(key=lambda x: x['points'], reverse=True)

    for user in users if users else []:
        try:
            await message.chat.get_member(user['_id'])
            
            for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
                    if char in user['username']:
                        user['username'] = user['username'].replace(char, "\\"+char)
            if user['username']:
                title += f"@{user['username']} — {user['points']}\n"
            else:
                for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
                    if char in user['first_name']:
                        user['first_name'] = user['first_name'].replace(char, "\\"+char)
                
                title += f"[{user['first_name']}](tg://user?id={user['_id']}) — user['points']"
        
        except exceptions.BadRequest:
            pass

    result = await message.reply(title)

    try:
        await result.pin(disable_notification=True)
    except exceptions.BadRequest:
        pass

    if (message.chat.type != 'private'):
        message.from_user = message.chat
        message.user['points'] = result.message_id
        await db.insertUser(message)

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
