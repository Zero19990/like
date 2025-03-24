import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, random
from user_agent import generate_user_agent

token = "5852388906:AAFYOkbMpkfBjyGi5sUzGZcTV0N9n5ToVws"
bot = telebot.TeleBot(token)

def is_valid_link(link):
    return link.startswith("https://")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("رشق 50 لايك", callback_data="request_likes")
    markup.add(button)
    bot.send_message(message.chat.id, "لطلب الرشق اضغط عل زر رشق 50 لايك", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "request_likes")
def ask_for_username(call):
    bot.send_message(call.message.chat.id, "ارسل يوزر حسابك عل انستكرام")
    bot.register_next_step_handler(call.message, process_username)

def process_username(message):
    user = message.text
    bot.send_message(message.chat.id, "ارسل رابط المنشور الذي تريد رشقه")
    bot.register_next_step_handler(message, lambda msg: process_link(msg, user))

def process_link(message, user):
    link = message.text
    if not is_valid_link(link):
        bot.send_message(message.chat.id, "الرابط غير صالح. تأكد أنه يبدأ بـ https://")
        return

    email = random.randint(100000, 999999)
    res = requests.post('https://api.likesjet.com/freeboost/7', json={
        'instagram_username': user, 
        'link': link, 
        'email': f'{email}@gmail.com'}, 
        headers={
            'Host': 'api.likesjet.com', 
            'content-length': '137', 
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"', 
            'accept': 'application/json, text/plain, */*', 
            'content-type': 'application/json', 
            'sec-ch-ua-mobile': '?1', 
            'user-agent': generate_user_agent(), 
            'sec-ch-ua-platform': '"Android"', 
            'origin': 'https://likesjet.com', 
            'sec-fetch-site': 'same-site', 
            'sec-fetch-mode': 'cors', 
            'sec-fetch-dest': 'empty', 
            'referer': 'https://likesjet.com/', 
            'accept-language': 'en-XA,en;q=0.9,ar-XB;q=0.8,ar;q=0.7,en-GB;q=0.6,en-US;q=0.5'
        }
    )

    if 'You can only receive likes once per day.' in res.text:
        bot.send_message(message.chat.id,'يرجى المحاوله بعد 24 ساعه قبل طلب الرشق مرى اخرى ')
    elif 'Success! You will receive likes within next few minutes.' in res.text:
        uu = f'''
تم طلب الرشق
اسم المستخدم  : {user}
رابط المنشور {link}
الكميه 50 لايك

بواسطه @PY_50

'''
        bot.send_message(message.chat.id, uu)
    else:
        bot.send_message(message.chat.id, res.json().get('message', 'حدث خطأ غير متوقع.'))

#تمت بواسطه @PY_50   
bot.polling()
