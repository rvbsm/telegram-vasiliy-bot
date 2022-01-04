import motor.motor_asyncio
import asyncio
from aiogram.types import User

class MongoDB:
    def __init__(self, uri: str):
        client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        client.get_io_loop = asyncio.get_running_loop
        db = client['vasiliy-database']
        self.users = db['users']
        self.commands = db['commands']
    

    async def userInsert(self, user: User):
        doc = user.__dict__["_values"]

        doc["_id"] = doc.pop("id")

        if not (await self.userFind(doc["_id"])):
            if not "points" in doc:
                doc["points"] = 0
            result = await self.users.insert_one(doc)
        else:
            result = await self.users.update_one({"_id": doc["_id"]}, {"$set": doc})

        return result

    async def userFind(self, id: int):
        doc = await self.users.find_one({"_id": id})

        return doc if doc else None

    async def usersGet(self):
        doc_list = self.users.find({})

        return [doc["_id"] for doc in await doc_list.to_list(length=10)] if doc_list else None

    async def commandInsert(self, command: str, data: str):
        doc = {"command": command, "data": data}

        if not (await self.commandFind(command)):
            result = await self.commands.insert_one(doc)
        else:
            result = await self.commands.update_one({"command": command}, {"$set": doc})
        
        return result
    
    async def commandFind(self, command: str):
        doc = await self.commands.find_one({"command": command})

        return doc if doc else None
    
    async def commandsGet(self):
        doc_list = self.commands.find({})

        return [doc["command"] for doc in await doc_list.to_list(length=100)] if doc_list else None

    async def commandDelete(self, command: str):
        result = None
        if (await self.commandFind(command)):
            result = await self.commands.delete_one({"command": command})
        
        return result


    async def addPoint(self, user: User, points: int = 1):
        curPoint = await self.getPoint(user)

        result = await self.users.update_one({"_id": user["_id"]}, {"$set": {"points": curPoint + points}})
        
        
        return result
    
    async def remPoint(self, user: User, points: int = 1):
        return await self.addPoint(user, -points)
    
    async def getPoint(self, user: User):
        return (await self.userFind(user["_id"]))["points"]
