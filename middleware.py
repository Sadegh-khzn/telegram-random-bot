from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable , Any ,Awaitable
from models import get_user,insert_user

class Requirmenets(BaseMiddleware):
    def __init__(self):
        ...

    async def __call__(
            self,
            handler:Callable[[Message,dict[str,Any]],Awaitable[Any]],
            event:Message,
            data:dict[str,Any])-> Any:
        user = await get_user(event.from_user.id)
        if user is None:
            print("\nuser inserted\n")
            await insert_user(event.from_user.id, event.from_user.username,event.from_user.first_name,event.from_user.last_name)
        print("update is here")
        if user is not None and user.is_blocked:
            return
        
        await handler(event,data)
        