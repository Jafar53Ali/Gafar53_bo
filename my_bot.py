import logging
import os
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# 1. الإعدادات والتوكن (جلبناه من إعدادات Render لضمان الأمان)
TOKEN = os.environ.get('BOT_TOKEN', "8539100889:AAFu0ioT0TFbQhHaWcpBtimc2vo-3fNBa7E")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. الدوال المساعدة
def get_eid_countdown():
    eid_date = datetime(2026, 3, 20) 
    delta = eid_date - datetime.now()
    return delta.days

def get_weather_info():
    return "حالة الطقس في السودان حالياً: الجو صافي ومشرق ☀️، درجة الحرارة 31°م."

# 3. دالة البداية (Start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("خدماتي 🛠️", callback_data='services'), InlineKeyboardButton("طقس السودان 🌤️", callback_data='weather')],
        [InlineKeyboardButton("كم باقي للعيد؟ 🌙", callback_data='eid'), InlineKeyboardButton("تواصل معي خاص 📲", callback_data='contact_private')],
        [InlineKeyboardButton("موقعي الشخصي 🌐", url='https://gafaral.github.io/HTML-Website/')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_msg = f"أهلاً بك يا {update.effective_user.first_name}! ✨\n\nأنا جعفر بوت ، طورني Gafar Ali Hamid.\nاضغط على الأزرار أدناه للخدمات السريعة، اسألني الجديد شنو أو جرب تدردش معاي!"
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup)

# 4. معالج الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'services':
        await query.message.reply_text("🛠️ خدماتي تشمل تطوير الويب وبناء أنظمة الأتمتة الذكية.")
    elif query.data == 'weather':
        await query.message.reply_text(get_weather_info())
    elif query.data == 'eid':
        await query.message.reply_text(f"🌙 متبقي {get_eid_countdown()} يوم على عيد الفطر المبارك.")
    elif query.data == 'contact_private':
        await query.message.reply_text("📩 للتواصل الخاص، يمكنك مراسلتي هنا: @Your_User_Name")

# 5. معالج المحادثة
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if any(word in text for word in ["صباح الخير", "صباح النور"]):
        await update.message.reply_text("يا صباح الورد! يومك سعيد يا غالي 🌸")
    elif any(word in text for word in ["جديدك", "الجديد شنو"]):
        await update.message.reply_text("والله يا مان مافي جديد")
    elif any(word in text for word in ["السلام عليكم", "سلام", "هلا"]):
        await update.message.reply_text(f"{update.effective_user.first_name} وعليكم السلام ورحمة الله وبركاته! نورت 🖥️")
    elif any(word in text for word in ["كيفك", "اخبارك"]):
        await update.message.reply_text("أنا بخير جداً طول ما الكود شغال! أنت كيفك؟ 😊")
    else:
        await update.message.reply_text("فهمتك! بس حالياً أنا مبرمج أرد على تحايا معينة، جرب تضغط على الأزرار فوق.")

# 6. تشغيل المحرك بطريقة متوافقة مع Render
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat_handler))
    
    print("البوت يعمل الآن...")
    # استخدام run_polling مباشرة هو الأفضل في النسخ الحديثة
    application.run_polling(close_loop=False)
