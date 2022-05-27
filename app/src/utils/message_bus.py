from tkinter import E
from typing import Callable, List, Coroutine, Any
from pydantic import BaseModel
import asyncio


class BusMessage(BaseModel):

    payload: dict


class AbstractAsyncBusMessageHandler:

    async def handle_message(self, message: BusMessage):
        raise NotImplementedError("Method must be implemented in child class")


class AsyncMessageBus:

    def __init__(self) -> None:
        self.subscribers = []
        self.message_history: List[BusMessage] = []

    async def subscribe(self, message_handler: AbstractAsyncBusMessageHandler) -> None:
        self.subscribers.append(message_handler) 

    async def add_message(self, message: BusMessage) -> None:
        self.message_history.append(message)
        for subscriber in self.subscribers:
            try:
                await subscriber.handle_message(message)
            except Exception as e:
                print(e)



