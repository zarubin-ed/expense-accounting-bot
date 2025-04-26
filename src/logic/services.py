from models import user_ids, group_ids, group_members, debts
from peewee import IntegrityError

def add_user(user_id, username):
    """Добавляет нового пользователя"""
    try:
        user = user_ids.create(user_id=user_id, username=username)
        return user
    except IntegrityError:
        print(f"Пользователь с ID {user_id} уже существует.")
        return None

def add_group(group_id, chat_id):
    """Добавляет новую группу"""
    group = group_ids.create(group_id=group_id, chat_id=chat_id)
    return group

def add_group_members(member_id, chat_id, user_id):
    group_member = group_members.create(member_id=member_id, chat_id=chat_id, user_id=user_id)
    return group_ids





