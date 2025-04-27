from telegram import Update
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, CallbackContext
from handlers.handlers import *
from dotenv import load_dotenv
import os

def get_token():
    load_dotenv()
    return os.getenv("BOT_TOKEN")

def run_bot():
    TOKEN = get_token()
    #print(TOKEN)
    #updater = Updater(TOKEN)
    #dispatcher = updater.dispatcher
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("who_owes_me", who_owes_me))
    application.add_handler(CommandHandler("whom_do_i_owe", whom_do_I_owe))
    application.add_handler(CommandHandler("my_owe", my_owe))
    application.add_handler(CommandHandler("free_owe", free_owe))
    application.add_handler(CommandHandler("who_are_my_parents", who_are_my_parents))

    application.run_polling()
    
    # Останавливаем бота при нажатии Ctrl+C
    #application.idle()
