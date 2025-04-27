from telegram import Update, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from src.logic.services import *
from telegram.error import BadRequest

async def get_user_name_surname_by_id(user_id, update : Update, context: CallbackContext):
  chat_id = update.effective_chat.id
  user_id = int(user_id)
  user = await context.bot.get_chat_member(chat_id, user_id).user
  return f"{user.first_name} {user.last_name}"

async def get_id_by_nick(update, context, username):
  username = username.lstrip("@")
  member = await context.bot.get_chat_member(update.effective_chat.id, username)
  user = member.user
  return user.id
  
def who_owes_me(update : Update, context: CallbackContext):
  user_id = str(update.message.from_user.id)
  chat_id = str(update.effective_chat.id)
  data = who_owes_this_user(user_id, chat_id)
  answer = ""
  if not data or len(data) == 0:
    answer = "Тебе никто не должен :("
  else:
    answer = "Хорошо, вот список участников чата, которые тебе должны:"
    for debtor_id, debt_sum in data:
      try:
        debtor = get_user_name_surname_by_id(debtor_id, update, context)
        answer += "\n"
        answer += f"{debtor} должен {debt_sum} рублей"
      except Exception as e:
        continue
  if (answer == "Хорошо, вот список участников чата, которые тебе должны:"):
    answer = "Извини, я не вижу твоих должников"
  await update.message.reply_text(answer)
  
def whom_do_I_owe(update : Update, context: CallbackContext):
  user_id = str(update.message.from_user.id)
  chat_id = str(update.effective_chat.id)
  data = whom_does_this_user_owe(user_id, chat_id)
  answer = ""
  if not data or len(data) == 0:
    answer = "У тебя нет долгов :)"
  else:
    answer = "Хорошо, вот список участников чата, которым ты должен:"
    for creditor_id, debt_sum in data:
      try:
        creditor = get_user_name_surname_by_id(creditor_id, update, context)
        answer += "\n"
        answer += f"Пользователю {creditor} ты должен {debt_sum} рублей"
      except Exception as e:
        continue
  if (answer == "Хорошо, вот список участников чата, которым ты должен:"):
    answer = "Извини, я не вижу, кому ты должен"
  await update.message.reply_text(answer)

def check_if_username_in_chat(update, context, username):
  chat_id = update.effective_chat.id
  username = username.lstrip("@")
  try:
    await context.bot.send_message(
      chat_id = chat_id,
      text = f"Checking user @{username}",
      entities = [MessageEntity(type=MessageEntity.MENTION, offset=16, length=len(username)+1)]
      )
    return True
  except BadRequest:
    return False
  
def my_owe(update : Update, context: CallbackContext):
  user_id = str(update.message.from_user.id)
  chat_id = str(update.effective_chat.id)
  args = context.args
  answer = ""
  if not args:
    answer = "У этой команды должны быть параметры: ник пользователя, которому ты должен и сумма долга"
    await update.message.reply_text(answer)
    return
  if len(args) != 2:
    answer = "У этой команды должно быть ровно два параметра: ник пользователя, которому ты должен и сумма долга"
    await update.message.reply_text(answer)
    return
  creditorname = args[0].lstrip("@")
  debtsum = safe_make_float(args[1])
  creditor_id = safe_get_second_user_id(update, context, creditorname)
  if debtsum != None and crteditor_id != None:
    register_debt(user_id, creditor_id, chat_id, debtsum)

def free_owe(update : Update, context: CallbackContext):
  user_id = str(update.message.from_user.id)
  chat_id = str(update.effective_chat.id)
  args = context.args
  answer = ""
  if not args:
    answer = "У этой команды должны быть параметры: ник пользователя, который был тебе должен и сумма долга"
    await update.message.reply_text(answer)
    return
  if len(args) != 2:
    answer = "У этой команды должно быть ровно два параметра: ник пользователя, который был тебе должен и сумма долга"
    await update.message.reply_text(answer)
    return
  debtorname = args[0].lstrip("@")
  debtsum = safe_make_float(args[1])
  debtor_id = safe_get_second_user_id(update, context, debtorname)
  if debtsum != None and debtor_id != None:
    register_debt_free(debtor_id, user_id, chat_id, debtsum) 

def safe_get_second_user_id(update, context, username):
  if not check_if_username_in_chat(update, context, username):
    answer = "Упс, этого пользователя нет в чате. Попробуй проверить корректность ника!"
    await update.message.reply_text(answer)
    return
  user_id = ""
  try:
    user_id = str(get_id_by_nick(update, context, username))
    return user_id
  except Exception as e:
    answer = "Извини, я не вижу этого пользователя"
    await update.message.reply_text(answer)
    return
 
def safe_make_float(update, context, debtsum):
  try:
    debtsum = float(debtsum)
    return debtsum
  except Exception as e:
    answer = "Второй аргумент должен быть числом!"
    await update.message.reply_text(answer)
    return
