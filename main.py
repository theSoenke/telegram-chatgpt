#!/usr/bin/env python

import logging
import os
from datetime import datetime

from pychatgpt import Chat
from telegram import ChatAction, ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

chats = {}

"""Send a message when the command /start is issued."""
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def reply(update: Update, context: CallbackContext) -> None:
    logging.info('Replying')
    chat_id = update.effective_message.chat_id
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    if chat_id not in chats:
        if len(chats) >= 10:
            update.message.reply_text("Reached maximum number of chats")
            return
        else:
            email = os.environ.get("OPENAI_EMAIL")
            password = os.environ.get("OPENAI_PASSWORD")
            chats[chat_id] = Chat(email=email, password=password)

    answer = chats[chat_id].ask(update.message.text)
    update.message.reply_text(answer)

def main() -> None:
    token = os.environ.get("TOKEN")
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
