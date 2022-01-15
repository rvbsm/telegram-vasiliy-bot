from main import dp, db
from aiogram.types import Message
from aiogram.utils.exceptions import Throttled


@dp.message_handler(commands="addcom")
async def add_command(message: Message):
    if len(message.get_args()) < 2:
        return
    
    
    if '<' in message.text:
        message.text = message.text.replace('<', "&lt;")
    if '>' in message.text:
        message.text = message.text.replace('>', "&gt;")
    """
    for char in '_*[]()~`>#+-=|{}.!':
        if char in message.text:
            message.text = message.text.replace(char, "\\"+char)
    """
    command = await db.insertCommand(message)

    await message.reply("Добавлена команда <code>{0}</code>\n<b>Доступные команды:</b> \n<code>{1}</code>".format(command, '</code>\n<code>'.join(await db.getCommands(message))))

@dp.message_handler(commands="delcom")
async def del_command(message: Message):
    command = message.get_args().split()[0]

    if not command:
        return

    await db.deleteCommand(message)

    await message.reply("Удалена команда <code>{0}</code>".format(command))

@dp.message_handler(lambda message: message.text[0] in ('/', '!'))
@dp.throttled(rate=2)
async def user_commands(message: Message):
    command = message.text[1:].split()[0]
    if not (command in await db.getCommands(message)):
        return
        
    data = await db.getCommand(message)
    data = data['data']
        
    await message.reply(data)
