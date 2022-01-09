from main import dp, db
from aiogram.types import Message
from aiogram.utils.exceptions import Throttled


@dp.message_handler(commands="addcom")
async def add_command(message: Message):
    command = message.get_args().split()[0]
    data = ' '.join(message.get_args().split()[1:])
    
    if len(message.get_args()) < 2:
        return

    for char in ('_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!'):
        if char in message.text:
            message.text = message.text.replace(char, "\\"+char)

    await db.insertCommand(message)

    await message.reply("Добавлена команда \"{0}\"\nДоступные команды: \n{1}".format(command, '\n'.join(await db.getCommands(message))))

@dp.message_handler(commands="delcom")
async def del_command(message: Message):
    command = message.get_args().split()[0]

    await db.deleteCommand(message)

    await message.reply("Удалена команда \"{0}\"".format(command))

@dp.message_handler(lambda message: message.text[0] in ('/', '!'))
@dp.throttled(rate=2)
async def user_commands(message: Message):
    command = message.text[1:].split()[0]
    if not (command in await db.getCommands(message)):
        return
        
    data = await db.getCommand(message)
    data = data["data"]
        
    await message.reply(data)
