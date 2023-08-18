import asyncio
import json
import os

import aiofiles as aiofiles

from models import Message
from settings import settings


# Функция для создания файла отключения
async def create_disconnect_file() -> None:
    async with aiofiles.open(settings.APP_PATH + "/tmp/notifyDisconnect", "w") as f:
        await f.write("Disconnected")


# Функция для удаления файла отключения
async def remove_disconnect_file() -> None:
    if os.path.exists(settings.APP_PATH + "/tmp/notifyDisconnect"):
        os.remove(settings.APP_PATH + "/tmp/notifyDisconnect")


# Функция для отправки ответа с ошибкой
async def send_error(websocket, status: int, detail: str) -> None:
    data = {"detail": detail, "status": status}
    asyncio.create_task(websocket.send(data))


async def handle_client(websocket) -> None:
    """
    Обрабатывает соединение с клиентом
    """
    while True:
        try:
            data = await websocket.recv()
            message = Message(**json.loads(data))
            if message.action == "session_update":
                if not message.connected:
                    await websocket.send({"detail": "OK", "status": 200})
                    await asyncio.sleep(30)
                    if not message.connected:
                        await create_disconnect_file()
                elif message.connected:
                    await websocket.send({"detail": "OK", "status": 200})
                    await remove_disconnect_file()
            # Неверный запрос
            elif message.action != "session_update":
                await send_error(websocket, 400, "Bad request")
            # Успешная обработка
            else:
                await websocket.send({"detail": "OK", "status": 200})
        except:
            await send_error(websocket, 500, "Internal Server Error")
