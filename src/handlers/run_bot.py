from telegram import Update
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, CallbackContext
from handlers.handlers_mapping import handlers_by_name
from dotenv import load_dotenv
import os

def get_token():
    load_dotenv()
    return os.getenv("BOT_TOKEN")

def run_bot():
    TOKEN = get_token()
    
    application = Application.builder().token(TOKEN).build()
    
    command_names = ["who_owes_me", "whom_do_i_owe", "my_owe", "free_owe", "who_are_my_parents"]
    
    for command in command_names:
        application.add_handler(CommandHandler(command, handlers_by_name[command]))

    application.run_polling()
