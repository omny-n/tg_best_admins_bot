from typing import NamedTuple
from collections import defaultdict
import db
from sqlite3 import IntegrityError
import re
import exceptions

class Message(NamedTuple):
    """Структура распаршенного сообщения"""
    channel_name: str
    category_id: int
    channel_description: str


def get_admins_list() -> str:
    rows = db.fetchall()
    category_dict = defaultdict(list)
    for row in rows:
        category_dict[row[2]]
        for key in category_dict:
            if row[2] == key:
                category_dict[row[2]].append(row)
    sorted_list = []
    for key in category_dict.keys():
        sorted_list.append(f'\n▫️{key}')
        for value in category_dict[key]:
            sorted_list.append(f'[{value[3]}] @{value[0]} - {value[1]}') # приводим к виду: [ID] @admin - channel
    result = '\n'.join(sorted_list)
    return result


def get_admins_channels(tg_id:int) -> str:
    admins = db.get_admins_channels_db(tg_id)
    if not admins:
        return "Тебя нет в списке"
    s = []
    for admin in admins:
        s.append(f"[{admin[4]}] @{admin[0]} | {admin[1]} ({admin[2]}) – {admin[3]}")
    result = '\n'.join(s)
    return result


def get_categories_list() -> str:
    categories = db.get_categories_list_db()
    s = []
    for cat in categories:
        s.append(f"{cat[0]} - {cat[1]} - {cat[2]}")
    result = '\n'.join(s)
    return result


def add_admins_channels(tg_id:int, username:str, first_name:str, last_name:str, text_msg:str) -> str:
    parsed_message = _parse_add_msg(text_msg)
    check_admin = db.check_admin_in_db(tg_id)
    """Если админ есть в базе, то доабавляем только канал, если нет, то добавляем и инфо об админе"""
    try:
        if check_admin == None:
            column_list = (
                tg_id, 
                username, 
                first_name, 
                last_name, 
                parsed_message.channel_name, 
                parsed_message.category_id, 
                parsed_message.channel_description)
            db.add_admins_add_channels_db(column_list)
        else:
            column_list = (
                parsed_message.channel_name, 
                parsed_message.category_id, 
                parsed_message.channel_description,
                check_admin[0])
            db.add_channels_db(column_list)
        return 'Канал успешно добавлен в базу'
    except IntegrityError:
        return 'Такой канал уже есть в базе'        


def search_channel(raw_msg:str) -> str:
    """Поиск канала по названию"""
    parsed_text = _parse_search_channel_msg(raw_msg)
    search_result = db.search_channel_db(parsed_text)
    if not search_result:
        return "По запросу ничего не найдено"
    s = []
    for row in search_result:
        s.append(f"[{row[4]}] @{row[0]} | {row[1]} ({row[2]}) – {row[3]}")
    result = '\n'.join(s)
    return result

def delete_admins_channel(raw_msg:str) -> str:
    """Удаление выбранного канала, удалять могут только админы чата"""
    parsed_msg = _parse_del_channel_msg(raw_msg)
    del_msg = db.delete_channel(parsed_msg)
    if del_msg[0] == 1:
        return "Канал успешно удален."
    else:
        return "Канала с таким ID нет."


def _parse_search_channel_msg(text_msg:str) -> str:
    regexp_result = re.match(r"/search\s+(\w+)", text_msg)
    if not regexp_result:
        text_error = 'Некорректное сообщение, попробуй еще раз.'
        raise exceptions.NotCorrectMessage(text_error)
    return regexp_result.group(1)
    

def _parse_del_channel_msg(text_msg:str) -> int:
    regexp_result = re.match(r"/del\s+(\d*)", text_msg)
    if not regexp_result:
        text_error = 'Некорректное сообщение, попробуй еще раз.'
        raise exceptions.NotCorrectMessage(text_error)
    return regexp_result.group(1)


def _parse_add_msg(text_msg:str) -> Message:
    regexp_result = re.match(r"/add\s+(\@\w{5,})\s*(\d*)\s*(.{,50})", text_msg)
    if not regexp_result:
        text_error = 'Некорректное сообщение, попробуй еще раз или смотри /help'
        raise exceptions.NotCorrectMessage(text_error)
    
    return Message( channel_name=regexp_result.group(1),
                    category_id=regexp_result.group(2),
                    channel_description=regexp_result.group(3))