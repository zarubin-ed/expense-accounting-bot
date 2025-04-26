import sqlite3
import os
from peewee import SqliteDatabase
from models import proxy, user_ids, group_ids, group_members, debts

def __init__():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'expenses.db')

    db = SqliteDatabase(db_path)
    proxy.initialize(db)
    db.create_tables([user_ids, group_ids, group_members, debts])
    print('Data base have been initialized!')
