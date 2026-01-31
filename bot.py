import telebot
from telebot import types
from flask import Flask
import threading
import os
import time

# --- НАСТРОЙКИ ---
# Твой токен
TOKEN = '8443611271:AAHQiXYvsOGI5FuoEB-Q0QTgdKleskhS1QQ'
# Ссылка, которая РАБОТАЕТ в BotFather (скопируй её в точности!)
APP_URL = 'https://dandrusenko2005-ops.github.io/FireLiQ/'
# Твой канал
CHANNEL_URL = 'https://t.me/liquidjesus'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Веб-сервер для "здоровья" Koyeb
@app.route('/')
def health():
    return "OK", 200

@bot.message_handler(commands=['start'])
def start(message):
    try:
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # Кнопка WebApp
        web_app = types.WebAppInfo(APP_URL.strip())
        btn_shop = types.InlineKeyboardButton("ОТКРЫТЬ МАГАЗИН 🔥", web_app=web_app)
        
        # Кнопка канала
        btn_channel = types.InlineKeyboardButton("НАШ КАНАЛ 📢", url=CHANNEL_URL)
        
        markup.add(btn_shop, btn_channel)
        
        welcome_text = (
            f"Привет, {message.from_user.first_name}! 👋\n\n"
            "Добро пожаловать в **FireLiQ Store**.\n"
            "Теперь вы можете делать заказ с доставкой 24/7!"
        )
        
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"Error in start command: {e}")

def run_bot():
    while True:
        try:
            print("Бот запускается...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Ошибка бота: {e}")
            time.sleep(5)  # Пауза перед перезапуском при сбое

if __name__ == "__main__":
    # Запускаем бота в фоне
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем сервер на порту Koyeb
    # ВАЖНО: Порт должен быть 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

