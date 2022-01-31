from telegram import Bot, BotCommand
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CommandHandler

from text import text_messages


def get_token() -> str:
    with open('token.txt', 'r') as f:
        token = f.readline().strip()
    return token


def get_updater(token: str) -> Updater:
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    text_handler = MessageHandler(Filters.text & (~Filters.command), text_messages)
    dispatcher.add_handler(text_handler)

    #deadinside_handler = CommandHandler('1000minus7', deadinside)
    #dispatcher.add_handler(deadinside_handler)

    return updater
