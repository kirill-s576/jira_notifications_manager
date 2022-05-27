import os
from src.utils.message_bus import AsyncMessageBus


WS_MESSAGE_BUS = AsyncMessageBus()

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")
SERVER_SSL = os.getenv("SERVER_SSL")
