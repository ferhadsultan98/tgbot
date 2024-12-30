from flask import Flask, render_template
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import instaloader
from threading import Thread
import os

# Flask Uygulaması
app = Flask(__name__)  # Flask uygulamanız burada tanımlanıyor

# Telegram bot tokenınızı buraya yazın
TOKEN = '7776707741:AAF_ZKRfjt-yGn2fYJVwXfCQZtg95vaAxDA'

# Instagram video ve fotoğraf indirmek için instaloader
loader = instaloader.Instaloader()

# Kullanıcıları kaydedeceğimiz dosya
USER_FILE = 'users.txt'

# Logging
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask index route
@app.route('/')
def index():
    return render_template('index.html')

# Telegram botunu çalıştıracak fonksiyon
def run_telegram_bot():
    # Application kullanımı
    application = Application.builder().token(TOKEN).build()

    # Komutları bağla
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))

    # Botu başlat
    application.run_polling(drop_pending_updates=True)  # Bu metot daha verimli bir polling sağlar

# Flask ve Telegram botunu paralel çalıştırma
def main():
    # Flask'ı ayrı bir thread'de çalıştırıyoruz
    flask_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': True, 'use_reloader': False})
    flask_thread.start()

    # Telegram botunu çalıştır
    run_telegram_bot()

if __name__ == '__main__':
    main()
