from telebot import TeleBot
from telebot import types
from time import *

bot = TeleBot(' ')

with open('logfile.log', 'a', encoding="utf-8") as f_log:
    print(asctime(), 'Бот запущен', file=f_log)

def start_log(message: types.Message):
    with open('logfile.log', 'a', encoding="utf-8") as f_log:
        print(asctime(), f'Пользователь ({message.from_user.id}) прислал сообщение: {message.text}', file=f_log)

def do_log(query):
    with open('logfile.log', 'a', encoding="utf-8") as f_log:
        print(asctime(), f'Пользователь ({query.from_user.id}) выбрал: {query.data}', file=f_log)

def res_log(value):
    with open('logfile.log', 'a', encoding="utf-8") as f_log:
        print(asctime(), f'Калькулятор выдал результат равный {value}', file=f_log)


value = ''
old_value = ''


keyboard = types.InlineKeyboardMarkup()


keyboard.row(
        types.InlineKeyboardButton(' ', callback_data=' '), 
        types.InlineKeyboardButton('C', callback_data='C'), 
        types.InlineKeyboardButton('<=', callback_data='<='), 
        types.InlineKeyboardButton('/', callback_data='/')) 

keyboard.row(
        types.InlineKeyboardButton('7', callback_data='7'), 
        types.InlineKeyboardButton('8', callback_data='8'), 
        types.InlineKeyboardButton('9', callback_data='9'), 
        types.InlineKeyboardButton('*', callback_data='*')) 

keyboard.row(
        types.InlineKeyboardButton('4', callback_data='4'), 
        types.InlineKeyboardButton('5', callback_data='5'), 
        types.InlineKeyboardButton('6', callback_data='6'), 
        types.InlineKeyboardButton('-', callback_data='-')) 

keyboard.row(
        types.InlineKeyboardButton('1', callback_data='1'), 
        types.InlineKeyboardButton('2', callback_data='2'), 
        types.InlineKeyboardButton('3', callback_data='3'), 
        types.InlineKeyboardButton('+', callback_data='+')) 

keyboard.row(
        types.InlineKeyboardButton('j', callback_data='j'), 
        types.InlineKeyboardButton('0', callback_data='0'), 
        types.InlineKeyboardButton(',', callback_data='.'), 
        types.InlineKeyboardButton('=', callback_data='=')) 


@bot.message_handler(commands=['start'])
def get_message(message): 
    start_log(message)   
    global value
    if value == '':
        bot.send_message(message.from_user.id, 'Приветствую, приятной работы!', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    try:
        do_log(query)
        global value, old_value
        data = query.data

        if data == 'no':
            pass
        if data == 'C':
            value = ''
        elif data == '<=':
            if value != '':
                value = value[:len(value)-1]
        elif data == '=':
            value = str(eval(value))
            res_log(value)            
        else:
            value += data
        if value != old_value:
            if value == '':
                bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0', reply_markup=keyboard)
            else:                
                bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value, reply_markup=keyboard)
                
              
        old_value = value            
        

      
      
  
    except SyntaxError:
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0', reply_markup=keyboard)
    except ZeroDivisionError:
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='на 0 делить нельзя', reply_markup=keyboard)
    

bot.polling(non_stop=True)
