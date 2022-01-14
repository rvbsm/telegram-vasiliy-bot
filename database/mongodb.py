from html import entities
import motor.motor_asyncio
import asyncio
from aiogram.types import Message


class MongoDB:
    def __init__(self, uri: str):
        client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        client.get_io_loop = asyncio.get_running_loop
        self.db = client['vasiliy-database']
        self.users = self.db['users']
        self.chats = self.db['chats']


    async def insertUser(self, message: Message):
        self.chat = self.db['users_' + str(message.chat.id)]

        user = message.from_user.to_python()
        chat = message.chat.to_python()
        user['_id'], chat['_id'] = user.pop('id'), chat.pop('id')

        user_exist = await self.getUser(user['_id'])
        if not (user_exist):
            if ('type', 'supergroup') not in user.items():
                user['from_chat'] = [message.chat.id]
            await self.users.insert_one(user)
        else:
            if (message.chat.id not in user_exist['from_chat']):
                if ('type', 'supergroup') not in user.items():
                    user['from_chat'] = user_exist['from_chat']
                    user['from_chat'].append(message.chat.id)
            await self.users.update_one({'_id': user['_id']}, {'$set': user})
        if 'from_chat' in user:   
            user.pop('from_chat')
        
        if not (await self.getUserFromChat(user['_id'], chat['_id'])):
            if not 'points' in user:
                user['points'] = 0

            result = await self.chat.insert_one(user)
        else:
            result = await self.chat.update_one({'_id': user['_id']}, {'$set': user})

        return result

    async def getUserFromChat(self, user_id: int, chat_id: int):
        self.chat = self.db['users_' + str(chat_id)]
        user = await self.chat.find_one({'_id': user_id})

        return user if user else None

    async def getUser(self, user_id: int):
        user = await self.users.find_one({'_id': user_id})

        return user if user else None

    async def getUsersFromChat(self, message: Message):
        self.chat = self.db['users_' + str(message.chat.id)]
        user_list = self.chat.find({})

        return [user['_id'] for user in await user_list.to_list(length=10)] if user_list else None

    async def getUsers(self):
        user_list = self.users.find({})

        return [user['_id'] for user in await user_list.to_list()] if user_list else None

    async def insertCommand(self, message: Message):
        self.commands = self.db['commands_' + str(message.chat.id)]

        message.text = message.html_text
        full_command = message.get_args().split()
        command, data = full_command[0], ' '.join(full_command[1:])

        doc = {'command': command, 'data': data}
        message.text = '/' + message.get_args()

        if not (await self.getCommand(message)):
            result = await self.commands.insert_one(doc)
        else:
            result = await self.commands.update_one({'command': command}, {'$set': doc})
        
        return result
    
    async def getCommand(self, message: Message):
        self.commands = self.db['commands_' + str(message.chat.id)]

        command = message.text.split()[0][1:].lower()
        
        doc = await self.commands.find_one({'command': command})

        return doc if doc else None
    
    async def getCommands(self, message: Message):
        self.commands = self.db['commands_' + str(message.chat.id)]

        doc_list = self.commands.find({})

        return [doc['command'] for doc in await doc_list.to_list(length=100)] if doc_list else None

    async def deleteCommand(self, message: Message):
        self.commands = self.db['commands_' + str(message.chat.id)]

        command = message.get_args().split()[0]

        result = None
        if (await self.getCommand(message)):
            result = await self.commands.delete_one({'command': command})
        
        return result


    async def addPoint(self, message: Message, points: int = 1):
        curPoint = await self.getPoint(message)
        self.chat = self.db['users_' + str(message.chat.id)]

        result = await self.chat.update_one({'_id': message.from_user.id}, {'$set': {'points': curPoint + points}})
        
        return result
    
    async def remPoint(self, message: Message, points: int = 1):
        return await self.addPoint(message, -points)
    
    async def getPoint(self, message: Message):
        return (await self.getUserFromChat(message.from_user.id, message.chat.id))['points']


    async def insertChat(self, message: Message):
        chat = message.chat.to_python()
        chat['_id'] = chat.pop('id')

        if not (await self.getChat(message)):
            return await self.chats.insert_one(chat)

        return await self.chats.update_one({'_id': chat['_id']}, {'$set': chat})

    async def getChat(self, message: Message):
        return await self.chats.find_one({'_id': message.chat.id})


    async def setTable(self, message: Message):
        await self.insertChat(message)
        
        return self.chats.update_one({'_id': message.chat.id}, {'$set': {'message_id': message.message_id}})

    async def getTable(self, message: Message):
        result = await self.chats.find_one({'_id': message.chat.id})
        if result:
            return result['message_id'] if 'message_id' in result else None
