from telegram import Update
from telegram.ext import CallbackContext

from parser import campus_parser


def text_messages(update: Update, context: CallbackContext) -> None:
    try:
        if update.message is None:
            return None
        elif update.message.chat.type == 'private' and len(update.message.text.split()) != 2:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Введіть логін і пароль через пробіл")
        elif update.message.chat.type == 'private' and len(update.message.text.split()) == 2:
            log_pass = update.message.text.split()
            lines = campus_parser(log_pass[0], log_pass[1])
            message_block = ""
            grade_sum = 0
            for i in range(len(lines)):
                lesson_name = lines[i][0]
                grade_date = lines[i][1]
                grade = lines[i][2]
                # TODO: add teacher name
                if lesson_name != lines[i-1][0]:
                    if i != 0:
                        message_block += f"Сума балів: {round(grade_sum, 3)}\n"
                        grade_sum = 0
                    message_block += f"\n*{lesson_name}*\n\n"

                message_block += f"{grade_date}  {grade}\n"
                # TODO: add norbal number checker
                grade_sum += float(grade.replace("н", "0").replace("+", "0").replace("-", "0"))
                if i == len(lines)-1:
                    message_block += f"Сума балів: {grade_sum}"

                if len(message_block) > 3800 or i == len(lines)-1:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=message_block,
                                             parse_mode="Markdown")
                    message_block = ""
    except AttributeError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Дані невірні")
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Щось зламалось")


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Цей бот парсить ваші оцінки з кампусу КПІ\n"
                                                                    "Введіть логін і пароль через пробіл")
