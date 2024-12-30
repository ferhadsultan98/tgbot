# bot.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import instaloader
import os

# Telegram bot tokenınızı buraya yazın
TOKEN = '7776707741:AAF_ZKRfjt-yGn2fYJVwXfCQZtg95vaAxDA'

# Instagram video ve fotoğraf indirmek için instaloader
loader = instaloader.Instaloader()

# Kullanıcıları kaydedeceğimiz dosya
USER_FILE = 'users.txt'

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Instagram video veya fotoğraf indirme fonksiyonu
def download_instagram_media(url):
    try:
        # URL üzerinden medya (fotoğraf, video) indirme
        shortcode = url.split("/")[-2]  # URL'den shortcode'u alıyoruz
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Medya tipi fotoğraf mı, video mu?
        if post.is_video:
            media_url = post.video_url
            return "video", media_url
        else:
            media_url = post.url
            return "photo", media_url
    except Exception as e:
        logger.error(f"Medya indirilirken hata oluştu: {e}")
        return None, None

# Kullanıcıları kaydedeceğimiz fonksiyon
def save_user(user_id):
    if not os.path.exists(USER_FILE):
        # Dosya yoksa oluştur
        with open(USER_FILE, 'w') as file:
            file.write(f"{user_id}\n")
    else:
        # Dosyaya ekle
        with open(USER_FILE, 'a') as file:
            file.write(f"{user_id}\n")

# /start komutu
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    # Kullanıcıyı kaydet
    save_user(user_id)
    
    await update.message.reply_text(
        "Salam. Zəhmət olmasa Instagram Linkinizi göndərin! ♥"
    )

# Video veya fotoğraf indirme ve gönderme
async def handle_instagram_link(update: Update, context: CallbackContext):
    url = update.message.text

    if 'instagram.com' in url:
        media_type, media_url = download_instagram_media(url)
        
        if media_type == "photo":
            # Fotoğraf ise gönder
            await update.message.reply_text("Şəklinizi tezliklə sizə təqdim edirəm.")
            await update.message.reply_photo(media_url)
        elif media_type == "video":
            # Video ise gönder
            await update.message.reply_text("Videonuzu tezliklə sizə təqdim edirəm.")
            await update.message.reply_video(media_url)
        else:
            # Medya tipi tanınmadıysa hata mesajı
            await update.message.reply_text("Doğru link göndərdiyindən əminsən dostum?.")
    else:
        await update.message.reply_text("Zəhmət olmasa doğru link göndərin.")

# Telegram botunu çalıştıracak fonksiyon
def run_telegram_bot():
    # Application kullanımı
    application = Application.builder().token(TOKEN).build()

    # Komutları bağla
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))

    # Botu başlat
    application.run_polling(drop_pending_updates=True)  # Bu metot daha verimli bir polling sağlar

if __name__ == '__main__':
    run_telegram_bot()
