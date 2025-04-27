from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from handlers.handlers import *
from dotenv import load_dotenv
import os

def get_token():
    load_dotenv()
    return os.getenv("BOT_TOKEN")

def run_bot():
    TOKEN = get_token()
    print(TOKEN)
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("who_owes_me", who_owes_me))
    dispatcher.add_handler(CommandHandler("whom_do_i_owe", whom_do_i_owe))
    dispatcher.add_handler(CommandHandler("my_owe", my_owe))
    dispatcher.add_handler(CommandHandler("free_owe", free_owe))

    updater.start_polling()
    
    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()