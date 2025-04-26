from models import User, Group, GroupMember, Debt
from peewee import IntegrityError

def add_user(username):
    """Добавляет нового пользователя"""
    try:
        user = User.create(username=username)
    except IntegrityError:
        print("Пользователь уже существует!")
        return None
    return user

def add_group(chat_id):
    """Добавляет новую группу"""
    group = Group.create(chat_id=chat_id)
    return group

def add_group_members(group_id, user_id):
    """Добавляет нового участника группы"""
    if get_group_member_id(group_id, user_id) != None:
        raise Exception("Такой участник группы уже был добавлен")
    group_member = GroupMember.create(group_id=group_id, user_id=user_id)
    return group_member

def add_depts(debtor_id, creditor_id, delta=0): 
    """Добавляет пару людей, """
    if (debtor_id.id == creditor_id.id):
        return None
    if debtor_id.group_id != creditor_id.group_id:
        raise Exception("Кредитор и должник должны быть в одной группе")
    debt = Debt.create(debtor_id=debtor_id, creditor_id=creditor_id, delta=delta)
    return debt

def get_user_id(username : str) -> int:
    try:
        user = User.get(User.username == username)
        return user.id
    except User.DoesNotExist:
        return add_user(username).id
    
def get_group_id(chat_id : str) -> int:
    try:
        group = Group.get(Group.chat_id == chat_id)
        return group.id
    except Group.DoesNotExist:
        return add_group(chat_id).id
    
def get_group_member_id(group_id : int, user_id : int) -> int:
    "Принимает id группы и id пользователя и возращает его id как участника группы"
    try:
        member = GroupMember.get((GroupMember.group_id == group_id) &
                                 (GroupMember.user_id == user_id))
        return member.id
    except GroupMember.DoesNotExist:
        return add_group_members(group_id, user_id).id
    
def get_member_id(username : str, chat_id : str) -> int:
    "принимает имя пользователя и id чата, возращает id участника группы"
    group_id = get_group_id(chat_id)
    
    user_id = get_user_id(username)
    
    return get_group_member_id(group_id, user_id)
    
def get_debts_by_member(member_id: int) -> list[Debt]:
    return list(Debt.select().where(
        (Debt.debtor_id == member_id) | 
        (Debt.creditor_id == member_id)
    ))

def get_debts_by_pair_of_members(member_id1: int, member_id2: int) -> list[Debt]:
    try:
        return Debt.get(
            ((Debt.debtor_id == member_id1) & (Debt.creditor_id == member_id2)) |
            ((Debt.debtor_id == member_id2) & (Debt.creditor_id == member_id1))
        )
    except Debt.DoesNotExist:
        return add_depts(member_id1, member_id2)

def get_group_member_by_id(member_id : int) -> GroupMember:
    return GroupMember.get_by_id(member_id)

def get_group_by_id(group_id : int) -> Group:
    return Group.get_by_id(group_id)

def get_user_by_id(user_id : int) -> User:
    return User.get_by_id(user_id)

def get_user_by_member_id(member_id : int) -> User:
    return get_user_by_id(get_group_member_by_id(member_id).user_id)

def make_dict_from_dept_list(debts : list, member_id : int, inverse : bool) -> dict[str, int]:
    result = dict()
    if inverse:
        for dept in debts:
            if dept.creditor_id == member_id:
                if dept.delta > 0:
                    result[get_user_by_member_id(dept.debtor_id)] = dept.delta
            else:
                if dept.delta < 0:
                    result[get_user_by_member_id(dept.creditor_id)] = -dept.delta
    else:
        for dept in debts:
            if dept.debtor_id == member_id:
                if dept.delta > 0:
                    result[get_user_by_member_id(dept.creditor_id)] = dept.delta
            else:
                if dept.delta < 0:
                    result[get_user_by_member_id(dept.debtor_id)] = -dept.delta
    return result

def get_owe_dict_impl(username : str, chat_id : str, inverse : bool) -> dict:
    member_id = get_group_member_id(username, chat_id)
    
    debts = get_debts_by_member(member_id)
    
    return make_dict_from_dept_list(debts, member_id, inverse)

def whom_does_this_user_owe(username : str, chat_id : str) -> dict:
    """
    whom_does_this_username_owe

    :param: username: Имя пользователя
    :type param: str
    :param: chat_id: Id чата, в котором состоит пользователь
    :type param: str
    :return: список пользователей-кредиторов с долгом нашего пользователя каждому из них
    :rtype: dict(str, int)
    """
    return get_owe_dict_impl(username, chat_id, False)

def who_owes_this_user(username : str, chat_id : str):
    """
    who_owes_this_user

    :param: username: Имя пользователя
    :type param: str
    :param: chat_id: Id чата, в котором состоит пользователь
    :type param: str
    :return: список пользователей, для кого данный пользователь является кредитором
    :rtype: dict(str, int)
    """
    return get_owe_dict_impl(username, chat_id, True)

def register_debt(debtor_username : str, creditor_username : str, chat_id : str, value : float):
    """
    register_debt 

    :param: debtor_username: имя должника
    :type param: string
    :param: creditor_username: имя кредитора
    :type param: string
    :param: chat_id: Id чата, в котором состоят эти пользователи
    :type param: str
    :param: value: сумма долга
    :type param: float
    :return: ничего не возвращает
    :rtype: void
    """
    debtor_member_id = get_group_member_id(debtor_username, chat_id)
   
    creditor_member_id = get_group_member_id(creditor_username, chat_id)

    debt = get_debts_by_pair_of_members(debtor_member_id, creditor_member_id)

    if debt.debtor_id != debtor_member_id:
        value = -value
    
    debt.delta += value
    debt.save()

def register_debt_free(debtor_username : str, creditor_username : str, chat_id : str, value : float):
    """
    register_debt_free

    :param: debtor_username: имя должника
    :type param: string
    :param: creditor_username: имя кредитора
    :param: chat_id: Id чата, в котором состоят эти пользователи
    :type param: str
    :type param: string
    :param: value: сумма долга
    :type param: int
    :return: ничего не возвращает
    :rtype: void
    """
    register_debt(debtor_username, creditor_username, -value)









