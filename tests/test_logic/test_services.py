import logic.services as ls
from db.__init__ import __init__
from pathlib import Path
import os

# PYTHONPATH=src python -m pytest --cov src tests --cov-report=term-missing

users = ['@denisbulgakow', '@egor_zarubin', '@ArtemS_31', 'тралалело тралала']
chats = ['id=888', 'id=88', 'id=8']
debts = [1000, -1000, 0, 300]

def clear_database():
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DB_PATH = PROJECT_ROOT / "src" / "db" / "expenses.db"
    try:
        os.remove(DB_PATH)
    except Exception:
        print("Базы данных не найдено")
    __init__()

def test_different_groups_disjointment():
    clear_database()
    for user1 in users:
        for user2 in users:
            ls.register_debt(user1, user2, chats[0], debts[0])
            ls.register_debt_free(user1, user2, chats[1], debts[3])

            assert ls.who_owes_this_user(user1, chats[2]) == {} and ls.whom_does_this_user_owe(user1, chats[2]) == {}
        
def test_debt_register():
    clear_database()
    for i in range(len(users)):
        ls.register_debt(users[0], users[i], chats[0], debts[i])
    
    assert {users[3] : debts[3]}  == ls.whom_does_this_user_owe(users[0], chats[0])
    
    assert {users[1] : -debts[1]} == ls.who_owes_this_user(users[0], chats[0])

    for i in range(len(users)):
        ls.register_debt_free(users[0], users[i], chats[0], debts[i])

    assert {}  == ls.whom_does_this_user_owe(users[0], chats[0])
    
    assert {} == ls.who_owes_this_user(users[0], chats[0])
    
def test_multiple_debts():
    clear_database()
    for i in range(len(users)):
        ls.register_debt(users[0], users[i], chats[0], debts[0])
    
    assert {users[3] : debts[0], users[2] : debts[0], users[1] : debts[0]}  == ls.whom_does_this_user_owe(users[0], chats[0])
    
    assert {} == ls.who_owes_this_user(users[0], chats[0])

def test_add_user():
    clear_database()

    for user in users:
        us = ls.add_user(user)
        assert us != None
    
    for user in users:
        us = ls.add_user(user)
        assert us == None

def test_from_real_case1():
    clear_database()
    ls.register_debt(users[0], users[1], chats[0], 8)
    ls.register_debt(users[0], users[1], chats[0], 6)
    ls.register_debt_free(users[0], users[1], chats[0], 6)
    ls.register_debt_free(users[0], users[1], chats[0], 100)

    res = ls.whom_does_this_user_owe(users[0], chats[0])
    
    assert res == {}

    res = ls.who_owes_this_user(users[0], chats[0])

    assert res == {users[1] : float(100 - 8)}