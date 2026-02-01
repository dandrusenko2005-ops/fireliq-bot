import telebot
from telebot import types
from flask import Flask
import threading
import os
import time

# --- КОНФИГУРАЦИЯ ---
TOKEN = '8443611271:AAHQiXYvsOGI5FuoEB-Q0QTgdKleskhS1QQ'
APP_URL = "https://dandrusenko2005-ops.github.io/FireLiQ"
CHANNEL_URL = "https://t.me/liquidjesus"

bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=4)
app = Flask(__name__)

@app.route('/')
def health():
    return "⚡ FireLiQ Bot is Active", 200

# Реакция на первое сообщение или кнопку СТАРТ
@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        # Создаем кнопки
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # Кнопка магазина (WebApp)
        web_app = types.WebAppInfo(APP_URL.strip())
        btn_shop = types.InlineKeyboardButton("🛍️ ОТКРЫТЬ МАГАЗИН", web_app=web_app)
        
        # Кнопка перехода в канал
        btn_channel = types.InlineKeyboardButton("🔥 НАШ КАНАЛ", url=CHANNEL_URL)
        
        markup.add(btn_shop, btn_channel)
        
        # Текст приветствия
        first_name = message.from_user.first_name
        welcome_msg = (
            f"Привет, {first_name}! 👋\n\n"
            "Рады видеть тебя в нашем магазине **FireLiQ🔥**.\n"
            "\n\n"
            "👇 **Чтобы начать покупки, нажми на кнопку ниже:**"
        )
        
        # Отправляем фото (если есть URL) или просто текст
        # Здесь мы используем текст с кнопкой
        bot.send_message(
            message.chat.id, 
            welcome_msg, 
            reply_markup=markup, 
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Error: {e}")

# Запуск постоянного опроса Telegram
def run_bot():
    print("Бот запущен...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

