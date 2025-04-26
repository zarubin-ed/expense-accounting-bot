from models import user_ids, group_ids, group_members, debts
from peewee import IntegrityError

def add_user(user_id, username):
    """Добавляет нового пользователя"""
    user = user_ids.create(username=username)
    return user

def add_group(group_id, chat_id):
    """Добавляет новую группу"""
    group = group_ids.create(chat_id=chat_id)
    return group

def add_group_members(chat_id, user_id):
    """Добавляет нового участника группы"""
    group_member = group_members.create(chat_id=chat_id, user_id=user_id)
    return group_member

def add_depts(debtor_id, creditor_id, delta=0): 
    """Добавляет пару людей, """
    if debtor_id.group_id != creditor_id.group_id:
        raise Exception("Кредитопр и должник должны быть в одной группе")
    debt = debts.create(debtor_id=debtor_id, creditor_id=creditor_id, delta=delta)
    return debt









