import telebot
import os
import requests

# جلب التوكن من إعدادات Render
TOKEN = os.environ.get('BOT_TOKEN')
# ضع مفتاح الطقس الخاص بك هنا
WEATHER_API_KEY = "ضع_مفتاح_الطقس_هنا" 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت الطقس! أرسل اسم المدينة بالإنجليزية (مثلاً: Khartoum) لمعرفة الحالة.")

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ar"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            bot.reply_to(message, f"الطقس في {city} حالياً:\n- درجة الحرارة: {temp}°C\n- الحالة: {desc}")
        else:
            bot.reply_to(message, "لم أتمكن من العثور على هذه المدينة، تأكد من الاسم بالإنجليزية.")
    except Exception as e:
        bot.reply_to(message, "حدث خطأ أثناء جلب البيانات.")

if __name__ == "__main__":
    print("البوت بدأ العمل...")
    bot.infinity_polling()
