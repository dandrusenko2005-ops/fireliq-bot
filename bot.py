import telebot
from telebot import types
from flask import Flask
import threading
import os

# --- ТВОИ НАСТРОЙКИ ---
TOKEN = '8443611271:AAHQiXYvsOGI5FuoEB-Q0QTgdKleskhS1QQ'

# ВНИМАНИЕ: Проверь эту ссылку! 
# Если кнопка из BotFather работает, скопируй ссылку оттуда и вставь сюда.
# Скорее всего, правильная ссылка выглядит так: https://dandrusenko2005-ops.github.io/
APP_URL = 'https://dandrusenko2005-ops.github.io/' 

CHANNEL_URL = 'https://t.me/liquidjesus'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running", 200

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Убеждаемся, что ссылка чистая, без лишних пробелов
    clean_url = APP_URL.strip()
    
    # Кнопка WebApp
    web_app = types.WebAppInfo(clean_url)
    btn_shop = types.InlineKeyboardButton("ОТКРЫТЬ МАГАЗИН 🛍️", web_app=web_app)
    
    # Кнопка канала
    btn_channel = types.InlineKeyboardButton("НАШ КАНАЛ 🔥", url=CHANNEL_URL)
    
    markup.add(btn_shop, btn_channel)
    
    welcome_text = (
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в **FireLiQ Store**.\n\n"
        "Жми кнопку ниже, чтобы зайти в магазин!"
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

def run_bot():
    print("Бот запущен...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

