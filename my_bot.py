from flask import Flask
from threading import Thread
import telebot
import os
import google.generativeai as genai  # إعدادات Gemini (موجودة ولن تتأثر)
from groq import Groq  # إضافة مكتبة Groq الجديدة
from datetime import datetime
from telebot import types

# --- إعداد السيرفر (Keep Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت و Gemini و Groq ---
TOKEN = "8539100889:AAFu0ioT0TFbQhHaWcpBtimc2vo-3fNBa7E"
bot = telebot.TeleBot(TOKEN)

# 1. إعداد Gemini (كما هو في كودك)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. إعداد Groq (المحرك الجديد لضمان الرد السريع)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# دالة حساب الأيام للعيد
def get_eid_countdown():
    eid_date = datetime(2026, 3, 20) 
    delta = eid_date - datetime.now()
    return max(0, delta.days)

# 1. رسالة الترحيب والأزرار (ممنوع اللمس كما طلبت)
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🌐 موقعي الشخصي", url="https://jafar53ali.github.io/Gafar53/")
    btn2 = types.InlineKeyboardButton("🛠️ خدماتي", callback_data='services')
    btn3 = types.InlineKeyboardButton("🌤️ طقس السودان", callback_data='weather')
    btn4 = types.InlineKeyboardButton("📲 تواصل معي خاص", callback_data='contact')
    btn5 = types.InlineKeyboardButton("🌙 متبقي للعيد", callback_data='eid')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    welcome_text = f"أهلاً بك يا {message.from_user.first_name}! ✨\nأنا جعفر بوت، طورني Gafar Ali Hamid كيف أقدر أساعدك اليوم؟"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# 2. معالج الأزرار (زي ما هو)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "services":
        bot.send_message(call.message.chat.id, "🛠️ خدماتي: تطوير مواقع، بناء بوتات ذكية، وأنظمة أتمتة.")
    elif call.data == "weather":
        bot.send_message(call.message.chat.id, "🌤️ طقس السودان: الجو مشمس وجميل، درجة الحرارة حوالي 31°م.")
    elif call.data == "contact":
        bot.send_message(call.message.chat.id, "📲 يمكنك مراسلتي مباشرة عبر: @Julie_53")
    elif call.data == "eid":
        days = get_eid_countdown()
        bot.send_message(call.message.chat.id, f"🌙 متبقي {days} يوم على عيد الفطر المبارك (20 مارس 2026).")

# 3. الدردشة المألوفة + الذكاء الاصطناعي (Groq كبديل أساسي)
@bot.message_handler(func=lambda message: True)
def chat(message):
    text = message.text.lower()
    
    # أوامرك القديمة (ممنوع اللمس)
    if any(word in text for word in ["سلام", "السلام عليكم", "هلا"]):
        bot.reply_to(message, "وعليكم السلام يا غالي! نورتني 🖥️")
    elif any(word in text for word in ["كيفك", "اخبارك"]):
        bot.reply_to(message, "أنا شغال مية مية الحمد لله، أنت أمورك كيف؟ 😊")
    elif any(word in text for word in ["جديدك", "الجديد شنو"]):
        bot.reply_to(message, "والله الجديد إننا شغالين على Render والوضع باسط! 😂")
    
    # لو الكلام مش من الأوامر القديمة، Groq (Llama 3) يجاوب لضمان السرعة
    else:
        try:
            # استخدام Groq للرد السريع بلهجة سودانية
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي ومرح، ترد باللغة العربية بلهجة سودانية."},
                    {"role": "user", "content": message.text}
                ],
            )
            bot.reply_to(message, completion.choices[0].message.content)
            
         # لو الكلام مش من الأوامر القديمة، Groq (Llama 3) يجاوب
    else:
        try:
            # ده السطر اللي هيخلي البوت ينطق فوراً
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي ومرح، ترد باللغة العربية بلهجة سودانية."},
                    {"role": "user", "content": message.text}
                ],
            )
            bot.reply_to(message, completion.choices[0].message.content)
            
        except Exception as e:
            # لو في مشكلة في Groq، جرب Gemini كخيار أخير
            try:
                response = model.generate_content(message.text)
                bot.reply_to(message, response.text)
            except Exception as e2:
                bot.reply_to(message, "يا هندسة، السيرفر حالياً مضغوط، جرب تسألني كمان دقيقة.")

# --- تشغيل البوت بنظام infinity_polling لضمان الاستقرار في Render ---
if __name__ == "__main__":
    keep_alive()
    print("البوت شغال بنظام Llama 3 و Gemini احتياطي...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
