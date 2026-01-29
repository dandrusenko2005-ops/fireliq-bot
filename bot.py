import telebot
from telebot import types
from flask import Flask
import threading
import os

# --- ТВОИ НАСТРОЙКИ ---
TOKEN = '8443611271:AAHQiXYvsOGI5FuoEB-Q0QTgdKleskhS1QQ'
# Ссылка на твой магазин (WebApp)
APP_URL = 'https://dandrusenko2005-ops.github.io/shop/' 
# Твой канал
CHANNEL_URL = 'https://t.me/liquidjesus' 

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# Маленький сервер для проверки работоспособности хостингом
@server.route("/")
def webhook():
    return "FireLiQ Bot is running!", 200

@bot.message_handler(commands=['start'])
def start(message):
    # Создаем кнопки под сообщением
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Кнопка 1: Открыть магазин (WebApp)
    web_app = types.WebAppInfo(APP_URL)
    btn_shop = types.InlineKeyboardButton("ОТКРЫТЬ МАГАЗИН 🛍️", web_app=web_app)
    
    # Кнопка 2: Перейти в канал
    btn_channel = types.InlineKeyboardButton("НАШ КАНАЛ 🔥", url=CHANNEL_URL)
    
    markup.add(btn_shop, btn_channel)
    
    welcome_msg = (
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в **FireLiQ Store**. 🔥\n"
        "У нас ты найдешь всё самое необходимое по лучшим ценам.\n\n"
        "Жми на кнопку ниже, чтобы зайти в магазин или подписаться на наш канал!"
    )
    
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode='Markdown')

def run_bot():
    # Запуск бесконечного цикла проверки сообщений
    bot.infinity_polling()

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    threading.Thread(target=run_bot).start()
    # Запускаем веб-сервер на порту, который выделит Render
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)

