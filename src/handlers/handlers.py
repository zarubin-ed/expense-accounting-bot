from telegram import Update, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from src.logic.services import who_owes_this_user, whom_does_this_user_owe, register_debt, register_debt_free
from telegram.error import BadRequest
import telegram

async def get_user_name_surname_by_id(user_id : str, update : Update, context: CallbackContext) -> str:
  """Получает имя и фамилию пользователя по его id"""
  chat_id = update.effective_chat.id
  user_id = int(user_id)
  user = await context.bot.get_chat_member(chat_id, user_id).user
  return f"{user.first_name} {user.last_name}"

async def who_owes_me(update : Update, context: CallbackContext) -> None:
  """Вывести список пользователей, которые должны тому, кто отправил команду"""
  username = update.effective_user.username.lstrip("@")
  chat_id = str(update.effective_chat.id)
  data = who_owes_this_user(username, chat_id)
  answer = ""
  if not data or len(data) == 0:
    answer = "Тебе никто не должен :("
  else:
    answer = "Хорошо, вот список участников чата, которые тебе должны:"
    for debtorname, debt_sum in data.items():
      try:
        answer += "\n"
        answer += f"{debtorname} должен {debt_sum} рублей"
      except Exception as e:
        continue
  if (answer == "Хорошо, вот список участников чата, которые тебе должны:"):
    answer = "Извини, я не вижу твоих должников"
  await update.message.reply_text(answer)
  
async def whom_do_I_owe(update : Update, context: CallbackContext) -> None:
  """Вывести список пользователей, которым должен этот"""
  username = update.effective_user.username.lstrip("@")
  chat_id = str(update.effective_chat.id)
  data = whom_does_this_user_owe(username, chat_id)
  answer = ""
  if not data or len(data) == 0:
    answer = "У тебя нет долгов :)"
  else:
    answer = "Хорошо, вот список участников чата, которым ты должен:"
    for creditorname, debt_sum in data.items():
      answer += "\n"
      answer += f"Пользователю {creditorname} ты должен {debt_sum} рублей"
  if (answer == "Хорошо, вот список участников чата, которым ты должен:"):
    answer = "Извини, я не вижу, кому ты должен"
  await update.message.reply_text(answer)

async def check_if_username_in_chat(update : Update, context: CallbackContext, username : str) -> bool:
  """Проверить, что этот пользователь писал что-то в чат"""
  username = username.lstrip('@')
  if '@' + username in update.message.text:
    return True
  return False
  
async def my_owe(update : Update, context: CallbackContext) -> None:
  """Регистрирует долг"""
  username = update.effective_user.username.lstrip("@")
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
  if not await check_if_username_in_chat(update, context, creditorname):
    answer = f"Извини, я не вижу этого пользователя. @{creditorname} должен сначала написать что-то в чат!"
    await update.message.reply_text(answer)
    return
  debtsum = await safe_make_float(update, context, args[1])
  if debtsum <= 0:
    answer = "Сумма долга положительна!"
    await update.message.reply_text(answer)
    return
  if username == creditorname:
    answer = "Что? Ты не можешь одолжить денег самому себе!"
    await update.message.reply_text(answer)
    return
  if debtsum != None:# and creditor_id != None:
    register_debt(username, creditorname, chat_id, debtsum)

async def free_owe(update : Update, context: CallbackContext) -> None:
  """Прощает долг"""
  username = update.effective_user.username.lstrip("@")
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
  if not await check_if_username_in_chat(update, context, debtorname):
    answer = f"Извини, я не вижу этого пользователя. @{creditorname} должен сначала написать что-то в чат!"
    await update.message.reply_text(answer)
    return
  if username == debtorname:
    answer = "Что? Ты не можешь простить долг сам себе!"
    await update.message.reply_text(answer)
    return
  debtsum = await safe_make_float(update, context, args[1])
  if debtsum == None:
    return
  if debtsum <= 0:
    answer = "Сумма долга положительна!"
    await update.message.reply_text(answer)
    return
  if debtsum != None:
    register_debt_free(debtorname, username, chat_id, debtsum) 

async def who_are_my_parents(update : Update, context: CallbackContext) -> None:
  """Пасхалка"""
  answer = "У меня два отца, Егор и Денис. Мамы у меня нет :)"
  await update.message.reply_text(answer)
 
async def safe_make_float(update : Update, context: CallbackContext, debtsum : str) -> float:
  """Делает дробное число из входа и кидает исключение, если это невозможно"""
  try:
    debtsum = float(debtsum)
    return debtsum
  except Exception as e:
    answer = "Второй аргумент должен быть числом!"
    await update.message.reply_text(answer)
    return 1.0
