import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext, Filters
import random
import json
from telegram.ext.dispatcher import run_async
import time
from main import dispatcher
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

ONE, TWO, THREE, FOUR, FIVE, *_ = range(100)

owners = [163494588,1223713950,1647842393]
registered_id = []
registered_name = []
judges = []
judges_id = []


def msg_judge(update , context):
    id = update.effective_user.id
    text = update.message.text.split()[1]
    if id in owners:
     for i in judges_id:
        context.bot.send_message(chat_id= i , text=text, parse_mode=ParseMode.HTML)
        
     update.message.reply_text('msg sent to all judges')
        
def msg_cont(update , context):
    id = update.effective_user.id
    text = update.message.text.split()[1]
    if id in owners:
     for i in registered_id:
         context.bot.send_message(chat_id= i , text=text, parse_mode=ParseMode.HTML)
        
     update.message.reply_text('msg sent to all contestant')
    

def credit(update , context):
    update.message.reply_text('Credit to <i>@wancoins</i> , my master who created me 😃', parse_mode = ParseMode.HTML)

def judge(update, context):
    count = 1
    list = '<b>Judges list</b>\n\n'

    for i in judges:
        list += f'{count}' + '.' + i + '\n'
        count += 1

    context.bot.send_message(chat_id=update.effective_chat.id, text=list, parse_mode=ParseMode.HTML)

def add_judge(update,context):
    id = update.effective_user.id
    to_id = update.message.reply_to_message.from_user.id
    to_name = update.message.reply_to_message.from_user.first_name
    if id in owners:
        judges.append(to_name)
        judges_id.append(to_id)
        update.message.reply_text(f"{to_name} is added to judges list")
    else:
        update.message.reply_text("not authorized")


def reset(update, context):
    id = update.effective_user.id
    type = update.message.text.split()[1]

    if id in owners:
        if type == 'contestant':
         registered_name.clear()
         registered_id.clear()
         update.message.reply_text('<b>The contestant list has been successfully cleared</b>', parse_mode=ParseMode.HTML)
         if type == 'judge':
             judges.clear()
             judges_id.clear()
             update.message.reply_text('<b>The judges list has been successfully cleared</b>',
                                       parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text('Not authorized')


def contestant(update, context):
    count = 1
    list = '<b>contestant list</b>\n\n'

    for i in registered_name:
        list += f'{count}' + '.' + i + '\n'
        count += 1

    context.bot.send_message(chat_id=update.effective_chat.id, text=list, parse_mode=ParseMode.HTML)


def start(update , context):
    update.message.reply_text('please use /register <title of event> to submit registration')

def register(update, context):
    cd = context.bot_data
    id = update.effective_user.id

    cd['name'] = name = update.effective_user.name
    cd['given_name'] = given_name = update.effective_user.first_name
    cd['id'] = id
    id = cd['id']

    try:
     password = update.message.text.split()[1]
     if id not in registered_id:
      if password.lower() == 'xmas':
       update.message.reply_text(f'welcome {name}\n\n'
                              f'You applied for {password} contest in @artkayo , make sure you joined the group and dont change your username'
                              f'\n\nA notification will be sent to you once your application is approved.')

      keyboard = [
          [InlineKeyboardButton("Approve ✅", callback_data='approve'),
           InlineKeyboardButton("Reject ❌", callback_data='reject'), ]
      ]

      reply_markup = InlineKeyboardMarkup(keyboard)

      context.bot.send_message(chat_id= -1001287435306, text=f'<b>New Ticket</b>\n\n'
                                                            f'<b>Username : {name}</b>\n'
                                                            f'<b>Submitted Name :</b> {given_name} \n<i>Want to participate the contest</i>\n'
                                                            f'Joined group @artkayo status :'
                                                            f' <b>YES</b>', parse_mode=ParseMode.HTML,
                               reply_markup=reply_markup)
     else:
         update.message.reply_text('You already got approved and your name already in /contestant list')
    except IndexError:
        update.message.reply_text('type /register <event>')


def register2(update, context):
    cd = context.bot_data
    query = update.callback_query
    uname = cd['name']
    given_name = cd['given_name']
    name = update.callback_query.from_user.first_name
    id = cd['id']

    if query.data == 'reject':
        query.edit_message_text(f'<b>New Ticket</b>\n\n'
                                f'<b>Username : {uname}</b>\n'
                                f'<b>Submitted Name :</b> {given_name} \n<i>Want to participate the contest</i>\n'
                                f'Joined group @artkayo status :'
                                f' <b>YES</b>\n\n'
                                f'Rejected  ❌\n'
                                f'by : {name}', parse_mode = ParseMode.HTML)
        context.bot.send_message(chat_id=id, text=f'Sorry , your ticket has been rejected, '
                                                  f'check either you submit wrong info or you did not join the group'
                                                  f'\n\nyou can send a new ticket\n\nHave a nice day', parse_mode = ParseMode.HTML)

    elif query.data == 'approve':
        registered_id.append(id)
        registered_name.append(uname)
        query.edit_message_text(f'<b>New Ticket</b>\n\n'
                                f'<b>Username : {uname}</b>\n'
                                f'<b>Submitted Name :</b> {given_name} \n<i>Want to participate the contest</i>\n'
                                f'Joined group @artkayo status :'
                                f' <b>YES</b>\n\n'
                                f'Approved  ✅\n'
                                f'by : {name}', parse_mode = ParseMode.HTML)
        context.bot.send_message(chat_id=id,
                                 text=f'Congratulation , you have been approved, you are now listed in /contestant'
                                      f'\nMake sure to check pin message in @artkayo for more info regarding contest')



REG1_HANDLER = CommandHandler('register', register)
CONTESTANT_HANDLER = CommandHandler('contestant', contestant)
RESET_HANDLER = CommandHandler('reset', reset)
START_HANDLER = CommandHandler('start', start)
JUDGE_HANDLER = CommandHandler('judge', judge)
ADD_JUDGE_HANDLER = CommandHandler('add_judge', add_judge)
CREDIT_HANDLER = CommandHandler('credit', credit)
MSG_JUDGE_HANDLER = CommandHandler('msg_judge', msg_judge)
MSG_CONT_HANDLER = CommandHandler('msg_cont', msg_cont)

dispatcher.add_handler(REG1_HANDLER)
dispatcher.add_handler(CallbackQueryHandler(register2))
dispatcher.add_handler(RESET_HANDLER)
dispatcher.add_handler(CONTESTANT_HANDLER)
dispatcher.add_handler(START_HANDLER)
dispatcher.add_handler(JUDGE_HANDLER)
dispatcher.add_handler(ADD_JUDGE_HANDLER)
dispatcher.add_handler(CREDIT_HANDLER)
dispatcher.add_handler(MSG_CONT_HANDLER)
dispatcher.add_handler(MSG_JUDGE_HANDLER)
