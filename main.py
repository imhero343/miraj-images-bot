from socket import timeout
from PIL import Image
from blend_modes import multiply
import numpy as np
import telebot

import time


def imgProcessor(logoName='wide'):
    # اجيب الصور
    filename = f'{logoName}.png'
    logo = 'logo.png'
    filename1 = 'image.jpg'
    frontImage = Image.open(filename)
    img = Image.open(filename1)
    thelogo = Image.open(logo)
    # حول الباككًراوند الى rgba
    background = img.convert("RGBA")
    # غير حجم الجريدينت
    new = frontImage.resize((background.width, background.height))
    # حول الى نمباي
    np_bg = np.array(background)
    np_foreground = np.array(new)
    #  انتجر امج
    foreground_img_float = np_foreground.astype(float)
    np_bg_float = np_bg.astype(float)
    # فلوت امج
    new = multiply(np_bg_float, foreground_img_float, 1)

    # #  rontImage = frontImage.convert("RGBA")
    rgbalogo = thelogo.convert("RGBA")
    goodlogo = rgbalogo.resize(
        (round(rgbalogo.width/11), round(rgbalogo.height/11)))
    # new = multiply(background, new, 1)
    # # background.paste(new, (0, 0), new)
    blended_img = np.uint8(new)
    blended_img_raw = Image.fromarray(blended_img)
    blended_img_raw.paste(
        goodlogo, (background.width-130, background.height-165), goodlogo)
    # Image needs to be converted back to uint8 type for PIL handling.

    blended_img_raw.save('end.png')


bot = telebot.TeleBot(
    "5278615098:AAHTkdCOeqJU4DCVy5XA73huUOZKJy1x22Y", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """ اهلا بيك في بوت الصور
    عبدالله بالخدمة""")


@bot.message_handler(content_types=["photo"])
def verifyUser(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    height = message.photo[-1].height
    width = message.photo[-1].width
    ratio = height/width
    if ratio <= 0.7:
        imgProcessor('widex')
    if ratio > 0.71 and ratio < 0.9:
        imgProcessor('wide')
    if ratio < 1.6 and ratio > 1.1:
        imgProcessor('long')
    if ratio >= 1.6:
        imgProcessor('longx')
    if ratio == 1 or (ratio >= 0.9 and ratio <= 1.1):
        imgProcessor('square')
    new = open('end.png', 'rb')
    bot.send_photo(message.chat.id, new, timeout=10)


bot.infinity_polling()
