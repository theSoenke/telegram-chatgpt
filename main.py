#!/usr/bin/env python

import logging
import os
from datetime import datetime

from pychatgpt import Chat, OpenAI
from telegram import ChatAction, ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def reply(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)

    is_expired = OpenAI.token_expired()
    if is_expired:
        generate_token()

    answer = chat.ask(update.message.text)
    update.message.reply_text(answer)

def generate_token():
    now = datetime.now().strftime("%H:%M:%S")
    print("${now}: Generating new access token")

    email = os.environ.get("OPENAI_EMAIL")
    password = os.environ.get("OPENAI_PASSWORD")
    global chat
    chat = Chat(email=email, password=password)

def main() -> None:
    generate_token()

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    token = os.environ.get("TOKEN")
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
