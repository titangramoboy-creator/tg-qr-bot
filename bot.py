import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_H

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8752111202:AAG5grgyWQr5eF2NjREuWMD41jJnsCw_nWU"


def create_qr_with_logo(data, logo_path="logo.png"):
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=8,
        border=2,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#1565A3", back_color="white").convert('RGB')

    logo = Image.open(logo_path)

    qr_width, qr_height = img.size
    logo_size = qr_width // 4

    logo = logo.resize((logo_size, logo_size))

    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

    img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    file_path = "qr.png"
    img.save(file_path)

    return file_path


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    file_path = create_qr_with_logo(text)

    await update.message.reply_photo(photo=open(file_path, "rb"))


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот запущен...")
app.run_polling()