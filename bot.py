# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:54:30 2020

@author: Yen Zhe
"""
TOKEN= ''

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackContext
from telegram import InlineQueryResultArticle, InputTextMessageContent

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)




# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Bye!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def caps(update, context):
    """caps text after the command"""
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id,text=text_caps)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def inline_caps(update, context):
    """inline content"""
    query=update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)
    
def unknown(update,context):
    """returns message if message is unknown"""
    context.bot.send_message(chat_id=update.effective_chat.id,text="Sorry, I cannot understand")

def callback_10(context: CallbackContext):
    context.bot.send_message(chat_id=170148475,
                             text=" A message sent once with a 10s delay")

def callback_increasing(context: CallbackContext):
    job = context.job
    context.bot.send_message(chat_id=170148475,
                             text="Sending messages with a " + str(job.interval) +" s interval")
    job.interval += 1.0
    if job.interval > 10.0:
        job.schedule_removal()
    
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)
    j = updater.job_queue
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("caps",caps))
    dp.add_handler(InlineQueryHandler(inline_caps))
    
    # on noncommand
    dp.add_handler(MessageHandler(Filters.command, unknown))
    
    # log all errors
    dp.add_error_handler(error)
    
    j.run_once(callback_10, 10)
    j.run_repeating(callback_increasing,1)
    
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()