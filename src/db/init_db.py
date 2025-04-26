import sqlite3

def init_db():
    conn = sqlite3.connect('expenses.db')
    
    print('Data base have been initialized!')