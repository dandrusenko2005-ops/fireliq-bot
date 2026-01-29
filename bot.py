import telebot
from telebot import types
from flask import Flask
import threading
import os

# --- КОНФИГУРАЦИЯ ---
TOKEN = '8443611271:AAHQiXYvsOGI5FuoEB-Q0QTgdKleskhS1QQ'
APP_URL = 'https://t.me/Fireliqbot/FireLiQshop'
CHANNEL_URL = 'https://t.me/liquidjesus'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Маленький веб-сервер для Koyeb, чтобы сервис не засыпал и считался "Healthy"
@app.route('/')
def health_check():
    return "Bot is running", 200

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Кнопка WebApp (открывает магазин внутри ТГ)
    web_app = types.WebAppInfo(APP_URL)
    btn_shop = types.InlineKeyboardButton("ОТКРЫТЬ МАГАЗИН 🛍️", web_app=web_app)
    
    # Кнопка подписки на канал
    btn_channel = types.InlineKeyboardButton("НАШ КАНАЛ 🔥", url=CHANNEL_URL)
    
    markup.add(btn_shop, btn_channel)
    
    welcome_text = (
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в **FireLiQ Store**.\n"
        "Жми кнопку ниже, чтобы войти в приложение или перейти в канал."
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

def run_bot():
    print("Бот запущен...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Запускаем веб-сервер на порту, который требует Koyeb (обычно 8000 или 8080)
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

