import telebot
from telebot import types
from flask import Flask
import threading
import os
import time

# --- КОНФИГУРАЦИЯ ---
TOKEN = '8443611271:AAHQiXYvsOGI5FuoEB-Q0QTgdKleskhS1QQ'
APP_URL = 'https://dandrusenko2005-ops.github.io/shop/'
CHANNEL_URL = 'https://t.me/liquidjesus'

# Инициализируем бота с увеличенным таймаутом
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=4)
app = Flask(__name__)

# Хелсчек для хостинга и пинга
@app.route('/')
def health():
    return "⚡ FireLiQ Bot is Active and Fast", 200

@bot.message_handler(commands=['start'])
def start(message):
    try:
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # WebApp кнопка
        web_app = types.WebAppInfo(APP_URL.strip())
        btn_shop = types.InlineKeyboardButton("ОТКРЫТЬ МАГАЗИН 🛍️", web_app=web_app)
        btn_channel = types.InlineKeyboardButton("НАШ КАНАЛ 🔥", url=CHANNEL_URL)
        
        markup.add(btn_shop, btn_channel)
        
        welcome = (
            f"Привет, {message.from_user.first_name}! 👋\n\n"
            "Добро пожаловать в наш магазин **FireLiQ🔥**\n"
            "Заказывайте доставку через наш магазин 24/7"
        )
        
        bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"Start error: {e}")

def run_bot():
    print("Бот запущен в режиме Infinity Polling...")
    # infinity_polling автоматически перезапускается при ошибках сети
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    # Запуск бота в фоновом потоке
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Запуск Flask сервера (Koyeb будет его слушать)
    port = int(os.environ.get("PORT", 8000))
    # use_reloader=False важно при использовании потоков
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

