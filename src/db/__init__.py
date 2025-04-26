import os
import sqlite3

def __init__():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'expenses.db')

    

    print('Data base have been initialized!')