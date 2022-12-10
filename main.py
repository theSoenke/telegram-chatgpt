#!/usr/bin/env python

import logging
import os
from datetime import datetime

from pychatgpt import Chat
from telegram import ChatAction, ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from image_gen import text2image

MAX_MESSAGE_LENGTH = 4096
HELP_MESSAGE = """
Hello! Write me a message to get an answer to anything

You can use these additional commands:
/draw <prompt> - generate image
/reset - reset chat memory
/help - show help message
"""

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

email = os.environ.get("OPENAI_EMAIL")
password = os.environ.get("OPENAI_PASSWORD")
chat = Chat(email=email, password=password)
chat_map = {}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(HELP_MESSAGE)

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(HELP_MESSAGE)

def reset(update: Update, context: CallbackContext) -> None:
    logging.info('Resetting')
    chat_id = update.effective_message.chat_id
    if chat_id in chat_map[chat_id]:
        del chat_map[chat_id]

    update.message.reply_text("Chat memory has been reset")


def reply(update: Update, context: CallbackContext) -> None:
    logging.info('Replying')
    chat_id = update.effective_message.chat_id
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    if len(chat_map) >= 100:
        update.message.reply_text("Reached maximum number of chats")
        return

    previous_message_id, conversation_id = None, None
    if chat_id in chat_map:
        previous_message_id, conversation_id = chat_map[chat_id]

    answer, previous_message_id, conversation_id = chat.ask(
        update.message.text,
        previous_convo_id=previous_message_id,
        conversation_id=conversation_id
    )
    chat_map[chat_id] = [previous_message_id, conversation_id]

    parts = [answer[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(answer), MAX_MESSAGE_LENGTH)]
    for part in parts:
        update.message.reply_text(part)

def draw(update: Update, context: CallbackContext) -> None:
    logging.info('Drawing')
    chat_id = update.effective_message.chat_id
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    prompt = update.message.text.removeprefix("/draw").strip()
    photo = text2image(prompt)
    if photo != None:
        context.bot.send_photo(chat_id, photo=photo)
    else:
       update.message.reply_text("failed to generate image")

def main() -> None:
    token = os.environ.get("TOKEN")
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("draw", draw))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
