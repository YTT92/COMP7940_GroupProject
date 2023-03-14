from pymongo import MongoClient
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.ext import CallbackQueryHandler
import json
import re
# The messageHandler is used for all message updates
import configparser
import logging


global cluster
cluster = MongoClient("mongodb+srv://user_1:jz2BnwrOHwbKvn1H@parkingdata.p86fuwk.mongodb.net/?retryWrites=true&w=majority")
global db
db = cluster["hkparking"]
global collection
collection = db["data"]


def start(update, context):
    """Handler function for the /start command"""
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='講輸入想泊車的地區')


# Save as a parameter while user made the input
def input_location(update, context):
    location = update.message.text
    print(location)
    global collection
    # result = list(collection.find({'carpark_address': re.compile(fr"{location}")}))
    result = list(collection.find({'carpark_address': re.compile(fr"{location}")}))  #Select * from db where carpark_address = input
    # print(carpark_names)

    # number_of_result = collection.count_documents({'carpark_address': re.compile(fr"{location}")})
    # print(number_of_result)
    buttons=[]
    for i in range(len(result)):
        button = InlineKeyboardButton(text=result[i]['carpark_name'], callback_data=result[i]['carpark_name'])
        buttons.append([button])

    # create an InlineKeyboardMarkup object with the list of buttons
    keyboard = InlineKeyboardMarkup(buttons)

    # send the list of carpark names as a message with the keyboard
    update.message.reply_text('請選擇想要停泊的停車場:', reply_markup=keyboard)

# define a function to handle the button presses
def button(update, context):
    query = update.callback_query
    carpark_name = query.data
    global collection
    # find the document with the matching carpark name
    document = collection.find_one({'carpark_name': carpark_name})

    # get the carpark address from the document
    carpark_address = document['carpark_address']

    # send the carpark address as a message
    query.edit_message_text(text=f"地址: {carpark_address}")


def main():
# Load your token and create an Updater for your Bot
    updater = Updater(token=("6261863634:AAHcBD5htGdiC6BCu4-rxJBCYaLpQWw1qt4"), use_context=True)
    dispatcher = updater.dispatcher

# Add the command handler for the /start command
    dispatcher.add_handler(CommandHandler('start', start))
# Set up a message handler to call the save_location function
    message_handler = MessageHandler(Filters.text & ~Filters.command, input_location)
    dispatcher.add_handler(message_handler)

    # updater.dispatcher.add_handler(CommandHandler('list', input_location))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the bot
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()




