"""Аутентификация — бот работает только в выбранных чатах"""
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_id: int):
        self.access_id = access_id
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if int(message.chat.id) != int(self.access_id):
            await message.answer("Ну там же написано, что я бот чата лучших админов, вот там мне и пиши.")
            raise CancelHandler()