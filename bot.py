import logging
import os

import states
import exceptions

from aiogram import Bot, executor, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils.markdown import bold, code, text
from aiogram.types import ParseMode
from middlewares import AccessMiddleware

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger.error("Starting bot")

if not os.getenv("TELEGRAM_API_TOKEN"):
    exit("Error: no token provided. Terminated.")


bot = Bot(token=os.getenv("TELEGRAM_API_TOKEN"))
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(access_id=os.getenv("ACCESS_ID")))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    cat_list = states.get_categories_list()
    content = text(
        text('Привет,', bold(message.from_user.username), ', я бот чата лучших админов\.', 
        'Пока я умею не так много, но уже могу неплохо облегчить жизнь всему чату\.'),
        '',
        text('Для начала ознакомься с правилами, их не так много,', 
        'да и правилами их назвать можно с натяжкой, но они очень важны и без них тут все сломается\.',
        'Посмотреть правила можно командой\: /rules\.'),
        '',
        text('Когда насмотришься, добавь свой канал в базу, или каналы, сколько их там у тебя\.',
        'Сделать это можно командой:'),
        '',
        code('/add @канал код_котегории описание(50 до символов)'),
        '',
        text('К примеру: ', code('/add @durov 3 Канал Павла Дурова')),
        '',
        text('Описание можно не указывать, а вот без категорий пока никак, потом что\-нибудь придумаем\.',
        'Сейчас доступны следующие категории:'),
        '',
        code(f'{cat_list}'),
        '',
        text('Позже у админов чата будет возможность редактировать список категорий, а пока для этого надо толкать @Omny\_N'),
        '',
        text('Теперь, когда твой канал в базе, можешь использовать /my\_channels, чтобы показать его чату\.'),
        '',
        text('А еще ты можешь ответить командой /channels на любое сообщение в чате и я покажу каналы того, кому ты ответил\.'),
        '',
        text('Чтобы посмотреть весь список админов и их каналов, введи команду /list\. '
        'В списке ты увидешь ID канала, юзернейм админа и его канал, для удобства список разбит на категории\. '
        'Чтобы удалить канал, используй команду /del ID канала, удалять пока могут только администраторы чата\.'),
        '', 
        text('А еще я умею искать каналы в базе, просто напиши /search, а через пробел то что хочешь найти\.'),
        '',
        text('Совсем скоро я смогу еще больше\. :\)'),
        sep='\n')
    await message.reply(content, disable_notification=True, parse_mode=ParseMode.MARKDOWN_V2)

@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    answer_message = text('Правила:', 
        '1\. Хочешь позвать в конфу крутого админа? Сделай голосовалку за инвайт с его логином и юзеры конфы определят целесообразность этой затеи 👺',
        '2\. Час топа и не удалять из ленты это основополагающие столпы нашего общества\. ' 
        'Они приняты по умолчанию\. Если вам это НЕ подходит это обязательно обговаривать КАЖДЫЙ раз во избежание срача и гачи',
        '©️ Ivan',
        sep='\n')
    await message.reply(answer_message, disable_notification=True, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message_handler(commands=['list'])
async def get_admins_list(message: types.Message):
    """Показывает список администраторов и их каналов"""
    answer_message = states.get_admins_list()
    await message.answer(answer_message, disable_notification=True)


@dp.message_handler(commands=['channels'])
async def get_admins_channels(message: types.Message):
    """Показывает каналы каналы пользователя из реплая, либо каналы
    отправившего команду, если это не реплай"""
    if message.reply_to_message:
        tg_id = message.reply_to_message.from_user.id
    else:
        tg_id = message.from_user.id
    answer_message = states.get_admins_channels(tg_id)
    await message.reply(answer_message)


@dp.message_handler(commands=['my_channels'])
async def get_my_channels(message: types.Message):
    """Показывает каналы"""
    tg_id = message.from_user.id
    answer_message = states.get_admins_channels(tg_id)
    await message.reply(answer_message)


@dp.message_handler(filters.Text(startswith="/add "))
async def add_channels(message: types.Message):
    """Добавляет каналы в базу, парся регулярку вида:
        /add @channel_name 1 описание
        где 1 — айди категории
    """
    try:
        raw_message = states.add_admins_channels(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            message.text
            )
    except (exceptions.NotCorrectMessage) as e:
        await message.reply(str(e))
        return
    await message.reply(text(raw_message), parse_mode=ParseMode.MARKDOWN_V2)


@dp.message_handler(filters.Text(startswith='/del '), is_chat_admin=True)
async def delete_channels(message: types.Message):
    """Удаление канала из базы по айди"""
    try:
        answer = states.delete_admins_channel(message.text)
    except (exceptions.NotCorrectMessage) as e:
        await message.reply(str(e))
        return
    await message.answer(answer)


@dp.message_handler(filters.Text(startswith='/search '))
async def search_channels(message: types.Message):
    """Ищет каналы в базе по команде вида: /channels канал"""
    try:
        answer = states.search_channel(message.text)
    except (exceptions.NotCorrectMessage) as e:
        await message.reply(str(e))
        return
    await message.reply(answer)    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)