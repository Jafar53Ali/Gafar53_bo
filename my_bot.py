from flask import Flask
from threading import Thread
import telebot
import os
from groq import Groq  # استيراد مكتبة اللاما
from datetime import datetime
from telebot import types

# --- إعداد السيرفر (Keep Alive) لضمان بقاء البوت لايف في Render ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت و Groq (Llama 3) ---
TOKEN = "8539100889:AAFu0ioT0TFbQhHaWcpBtimc2vo-3fNBa7E"
bot = telebot.TeleBot(TOKEN)

# إعداد محرك Groq باستخدام المفتاح اللي ضفته في Render
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# دالة حساب الأيام للعيد
def get_eid_countdown():
    eid_date = datetime(2026, 3, 20) 
    delta = eid_date - datetime.now()
    return max(0, delta.days)

# 1. رسالة الترحيب والأزرار (كما هي دون تغيير)
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

# 2. معالج الأزرار
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

# 3. الدردشة المألوفة + Llama 3 (Groq)
@bot.message_handler(func=lambda message: True)
def chat(message):
    text = message.text.lower()
    
    # أوامرك الثابتة (ممنوع اللمس)
    if any(word in text for word in ["سلام", "السلام عليكم", "هلا"]):
        bot.reply_to(message, "وعليكم السلام يا غالي! نورتني 🖥️")
    elif any(word in text for word in ["كيفك", "اخبارك"]):
        bot.reply_to(message, "أنا شغال مية مية الحمد لله، أنت أمورك كيف؟ 😊")
    elif any(word in text for word in ["جديدك", "الجديد شنو"]):
        bot.reply_to(message, "والله الجديد إننا شغالين على Render والوضع باسطة! 😂")
    elif any(word in text for word in ["بيبي", "فطرتي ولا اشوي ليك قلبي"]):
        bot.reply_to(message, "بعد شنو تاني قايلها لي الساعة 8😒😒")
    elif any(word in text for word in ["بحبك", " ي عمري"]):
        bot.reply_to(message, "ونا بوت فيك ي روعة😍")
    
    # هنا الحقن الصافي لـ Llama 3
    else:
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي ومرح، ترد باللغة العربية بلهجة سودانية."},
                    {"role": "user", "content": message.text}
                ],
            )
            bot.reply_to(message, completion.choices[0].message.content)
        except Exception as e:
            bot.reply_to(message, "يا هندسة حالياً السيرفر مضغوط شوية، جرب تسألني بعد دقيقة.")

# --- تشغيل البوت بنظام infinity_polling لضمان الاستقرار التام ---
if __name__ == "__main__":
    keep_alive()
    print("البوت شغال بـ Llama 3 فقط...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
