# logic.py

from models import User, Group, Payment, Settlement
from peewee import IntegrityError
from datetime import date

def add_user(user_id, name):
    """Добавляет нового пользователя"""
    try:
        user = User.create(user_id=user_id, name=name)
        return user
    except IntegrityError:
        print(f"Пользователь с ID {user_id} уже существует.")
        return None

def add_group(group_id, name):
    """Добавляет новую группу"""
    group = Group.create(group_id=group_id, name=name)
    return group

def add_payment(payer_id, amount, group_id, payment_date):
    """Добавляет новый платеж"""
    payer = User.get(User.user_id == payer_id)
    group = Group.get(Group.group_id == group_id)
    payment = Payment.create(payer=payer, amount=amount, group=group, date=payment_date)
    return payment

def get_user_balance(user_id):
    """Получает баланс пользователя (сколько он должен и кому)"""
    user = User.get(User.user_id == user_id)
    settlements = Settlement.select().where(Settlement.user == user)
    balance = 0
    for settlement in settlements:
        balance += settlement.amount
    return balance

def settle_debt(user_id, amount):
    """Регистрирует расчёт долга для пользователя"""
    user = User.get(User.user_id == user_id)
    settlement = Settlement.create(user=user, amount=amount)
    return settlement
