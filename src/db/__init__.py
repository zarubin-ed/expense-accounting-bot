import os
from peewee import SqliteDatabase
from db.models import proxy, User, Group, GroupMember, Debt

def __init__():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'expenses.db')

    db = SqliteDatabase(db_path)
    proxy.initialize(db)
    db.create_tables([User, Group, GroupMember, Debt])
    print('Data base have been initialized!')
