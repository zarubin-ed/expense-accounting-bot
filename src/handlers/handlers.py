from telegram import Update, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from logic.services import *
from telegram.error import BadRequest
import telegram

async def get_user_name_surname_by_id(user_id, update : Update, context: CallbackContext):
  chat_id = update.effective_chat.id
  user_id = int(user_id)
  user = await context.bot.get_chat_member(chat_id, user_id).user
  return f"{user.first_name} {user.last_name}"

async def get_user_id_by_username(update, context, username):
    username = username.lstrip('@')
    chat = await context.bot.get_chat('@' + username)
    user_id = chat.id
    return user_id
  
async def who_owes_me(update : Update, context: CallbackContext):
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
        #debtor = await get_user_name_surname_by_id(debtor_id, update, context)
        answer += "\n"
        answer += f"{debtorname} должен {debt_sum} рублей"
      except Exception as e:
        continue
  if (answer == "Хорошо, вот список участников чата, которые тебе должны:"):
    answer = "Извини, я не вижу твоих должников"
  await update.message.reply_text(answer)
  
async def whom_do_I_owe(update : Update, context: CallbackContext):
  username = update.effective_user.username.lstrip("@")
  chat_id = str(update.effective_chat.id)
  data = whom_does_this_user_owe(username, chat_id)
  answer = ""
  if not data or len(data) == 0:
    answer = "У тебя нет долгов :)"
  else:
    answer = "Хорошо, вот список участников чата, которым ты должен:"
    for creditorname, debt_sum in data.items():
      #try:
      #creditor = await get_user_name_surname_by_id(creditor_id, update, context)
      answer += "\n"
      answer += f"Пользователю {creditorname} ты должен {debt_sum} рублей"
      #except Exception as e:
      #  continue
  if (answer == "Хорошо, вот список участников чата, которым ты должен:"):
    answer = "Извини, я не вижу, кому ты должен"
  await update.message.reply_text(answer)

async def check_if_username_in_chat(update, context, username):
  chat_id = update.effective_chat.id
  username = username.lstrip("@")
  try:
    msg = await context.bot.send_message(
      chat_id = chat_id,
      text = f"Checking user @{username}",
      entities = [{"type" : "mention", "offset" : 8, "length" : len(username) + 1}]
      )
    await msg.delete()
    return True
  except BadRequest:
    return False
  
async def my_owe(update : Update, context: CallbackContext):
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
    answer = "Извини, я не вижу этого пользователя"
    await update.message.reply_text(answer)
    return
  debtsum = await safe_make_float(update, context, args[1])
  if debtsum <= 0:
    answer = "Сумма долга положительна!"
    await update.message.reply_text(answer)
    return
  if username ==  creditorname:
    answer = "Что? Ты не можешь одолжить денег самому себе!"
    await update.message.reply_text(answer)
    return
  #creditor_id = await safe_get_second_user_id(update, context, creditorname)
  if debtsum != None:# and creditor_id != None:
    register_debt(username, creditorname, chat_id, debtsum)

async def free_owe(update : Update, context: CallbackContext):
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
  #debtor_id = await safe_get_second_user_id(update, context, debtorname)
  if debtsum != None:# and debtor_id != None:
    register_debt_free(debtorname, username, chat_id, debtsum) 

async def who_are_my_parents(update, context, username):
  answer = "У меня два отца, Егор и Денис. Мамы у меня нет :)"
  await update.message.reply_text(answer)

async def safe_get_second_user_id(update, context, username):
  if not await check_if_username_in_chat(update, context, username):
    answer = "Упс, этого пользователя нет в чате. Попробуй проверить корректность ника!"
    await update.message.reply_text(answer)
    return
  user_id = ""
  #try:
  user_id = str(await get_user_id_by_username(update, context, username))
  return user_id
  #except Exception as e:
  #  answer = "Извини, я не вижу этого пользователя"
  #  await update.message.reply_text(answer)
  #  return
 
async def safe_make_float(update, context, debtsum):
  try:
    debtsum = float(debtsum)
    return debtsum
  except Exception as e:
    answer = "Второй аргумент должен быть числом!"
    await update.message.reply_text(answer)
    return
