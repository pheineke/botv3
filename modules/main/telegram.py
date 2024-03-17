import json

import logging


from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


# Enable logging

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

# set higher logging level for httpx to avoid all GET and POST requests being logged

logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)



# Define a `/start` command handler.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message with a button that opens a the web app."""

    await update.message.reply_text(

        "Please press the button below to choose a color via the WebApp.",

        reply_markup=ReplyKeyboardMarkup.from_button(

            KeyboardButton(

                text="Open the color picker!",

                web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"),

            )

        ),

    )
