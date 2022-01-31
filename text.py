from telegram import Update
from telegram.ext import CallbackContext

from parser import campus_parser

def text_messages(update: Update, context: CallbackContext) -> None:
    if update.message is None:
        return None
    elif update.message.chat.type == 'private' and len(update.message.text.split()) == 2:
        log_pass = update.message.text.split()
        campus_parser(log_pass[0], log_pass[1])
        with open('pars.txt') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            context.bot.send_message(chat_id=update.effective_chat.id, text=lines[i])
