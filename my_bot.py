from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()




import telebot
import os
from datetime import datetime
from telebot import types

# التوكن بتاعك
TOKEN = "8539100889:AAFu0ioT0TFbQhHaWcpBtimc2vo-3fNBa7E"
bot = telebot.TeleBot(TOKEN)

# دالة حساب الأيام للعيد
def get_eid_countdown():
    eid_date = datetime(2026, 3, 20) 
    delta = eid_date - datetime.now()
    return max(0, delta.days)

# 1. رسالة الترحيب والأزرار الخمسة
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # إنشاء الأزرار الخمسة
    btn1 = types.InlineKeyboardButton("🌐 موقعي الشخصي", url="https://gafaral.github.io/HTML-Website/")
    btn2 = types.InlineKeyboardButton("🛠️ خدماتي", callback_data='services')
    btn3 = types.InlineKeyboardButton("🌤️ طقس السودان", callback_data='weather')
    btn4 = types.InlineKeyboardButton("📲 تواصل معي خاص", callback_data='contact')
    btn5 = types.InlineKeyboardButton("🌙 متبقي للعيد", callback_data='eid')
    
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    welcome_text = f"أهلاً بك يا {message.from_user.first_name}! ✨\nأنا  جعفر بوت، طورني Gafar Ali Hamidكيف أقدر أساعدك اليوم؟"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# 2. معالج الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "services":
        bot.send_message(call.message.chat.id, "🛠️ خدماتي: تطوير مواقع، بناء بوتات ذكية، وأنظمة أتمتة.")
    elif call.data == "weather":
        bot.send_message(call.message.chat.id, "🌤️ طقس السودان: الجو مشمس وجميل، درجة الحرارة حوالي 31°م.")
    elif call.data == "contact":
        bot.send_message(call.message.chat.id, "📲 يمكنك مراسلتي مباشرة عبر: @GafarAli")
    elif call.data == "eid":
        days = get_eid_countdown()
        bot.send_message(call.message.chat.id, f"🌙 متبقي {days} يوم على عيد الفطر المبارك (20 مارس 2026).")

# 3. الدردشة المألوفة
@bot.message_handler(func=lambda message: True)
def chat(message):
    text = message.text.lower()
    if any(word in text for word in ["سلام", "السلام عليكم", "هلا"]):
        bot.reply_to(message, "وعليكم السلام يا غالي! نورتني 🖥️")
    elif any(word in text for word in ["كيفك", "اخبارك"]):
        bot.reply_to(message, "أنا شغال مية مية الحمد لله، أنت أمورك كيف؟ 😊")
    elif any(word in text for word in ["جديدك", "الجديد شنو"]):
        bot.reply_to(message, "والله الجديد إننا شغالين على Render والوضع باسط! 😂")
    else:
        bot.reply_to(message, "كلامك سمح، بس جرب اضغط على الأزرار فوق عشان تشوف خدماتي.")

if __name__ == "__main__":
    print("جعفر بوت بدأ العمل...")
    bot.infinity_polling()


from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
