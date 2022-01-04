from bot import dp, db
from aiogram import types


@dp.message_handler(commands="addcom")
async def add_command(message: types.Message):
    command = message.get_args().split()[0]
    data = ' '.join(message.get_args().split()[1:])
    
    for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
        if char in data:
            data = data.replace(char, "\\"+char)

    await db.commandInsert(command, data)

    await message.reply("Добавлена команда \"{0}\"\nДоступные команды: {1}".format(command, await db.commandsGet()))

@dp.message_handler(commands="delcom")
async def del_command(message: types.Message):
    command = message.get_args().split()[0]

    await db.commandDelete(command)

    await message.reply("Удалена команда \"{0}\"".format(command))

@dp.message_handler(lambda message: message.text[0] in ('/', '!'))
async def user_commands(message: types.Message):
    command = message.text[1:].split()[0]
    if not (command in await db.commandsGet()):
        return
    
    data = await db.commandFind(command)
    data = data["data"]
    
    await message.reply(data)
