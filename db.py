import os
import sqlite3
from typing import Tuple


conn = sqlite3.connect(os.path.join("db", "data.db"))
cursor = conn.cursor()


def fetchall() -> list:
    cursor.execute('''
        SELECT  
            admins.admin_username,
            channels.channel_name,
            categories.title,
            channels.channel_id
        FROM
            channels
        inner join admins on channels.admin_id = admins.admin_id
        inner join categories on channels.category_id == categories.category_id
        order by admin_username
    ''')
    result = cursor.fetchall()
    return result


def get_admins_channels_db(tg_id:int) -> list:
    sql = '''
        SELECT  
            admins.admin_username,
            channels.channel_name,
            channels.description,
            categories.title,
            channels.channel_id
        FROM
            channels
        inner join admins on channels.admin_id = admins.admin_id
        inner join categories on channels.category_id == categories.category_id
        WHERE admins.tg_id = ?
        ;'''
    cursor.execute(sql, (tg_id,))
    result = cursor.fetchall()
    return result


def get_categories_list_db() -> list:
    sql = '''SELECT * from categories;'''
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def check_admin_in_db(tg_id:int) -> int:
    sql = '''SELECT admin_id FROM admins WHERE tg_id = ?;'''
    cursor.execute(sql, (tg_id,))
    result = cursor.fetchone()
    return result


def add_admins_add_channels_db(column_values: Tuple):
    sql = ''' 
        INSERT INTO admin_and_channels (
            tg_id, 
            admin_username, 
            admin_first_name, 
            admin_last_name, 
            channel_name, 
            category_id, 
            description
            )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ;'''
    cursor.execute(sql, column_values)
    conn.commit()


def add_channels_db(column_values: Tuple):
    sql = ''' 
        INSERT INTO channels ( 
            channel_name, 
            category_id, 
            description,
            admin_id
            )
        VALUES (?, ?, ?, ?)
        ;'''
    cursor.execute(sql, column_values)
    conn.commit()


def delete_channel(tg_id:int) -> int:
    cursor.execute("delete from channels where channel_id = ?", (tg_id,))
    cursor.execute("select changes()")
    result = cursor.fetchone()
    conn.commit()
    return result


def search_channel_db(search_row:str) -> tuple:
    sql = ''' 
        SELECT  
            admins.admin_username,
            channels.channel_name,
            channels.description,
            categories.title,
            channels.channel_id
        FROM
            channels
        inner join admins on channels.admin_id = admins.admin_id
        inner join categories on channels.category_id == categories.category_id
        WHERE channels.channel_name like ?
        ;'''
    cursor.execute(sql, (f'%{search_row}%',))
    result = cursor.fetchall()
    return result