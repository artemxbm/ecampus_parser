from telegram import Update
from telegram.ext import CallbackContext

from parser import campus_parser


def text_messages(update: Update, context: CallbackContext) -> None:
    if update.message is None:
        return None
    elif update.message.chat.type == 'private' and len(update.message.text.split()) == 2:
        log_pass = update.message.text.split()
        lines = campus_parser(log_pass[0], log_pass[1])
        message_block = ""
        for i in range(len(lines)):
            message_block += f"{lines[i][0]} {lines[i][2]}\n"
            if len(message_block) > 3800 or i == len(lines)-1:
                context.bot.send_message(chat_id=update.effective_chat.id, text=message_block)
                message_block = ""
