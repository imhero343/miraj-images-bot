from PIL import Image
import telebot


def imgProcessor(logoName='wide'):
    filename = f'{logoName}.png'
    filename1 = 'image.jpg'
    frontImage = Image.open(filename)
    img = Image.open(filename1)
    frontImage = frontImage.convert("RGBA")
    background = img.convert("RGBA")
    new = frontImage.resize((background.width, background.height))
    background.paste(new, (0, 0), new)
    background.save('end.png')


bot = telebot.TeleBot(
    "5278615098:AAHTkdCOeqJU4DCVy5XA73huUOZKJy1x22Y", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=["photo", 'document'])
def verifyUser(message):
    print(message.photo[-1].height)
    print(message.photo[-1].width)
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    height = message.photo[-1].height
    width = message.photo[-1].width
    ratio = height/width
    if ratio <= 0.75:
        imgProcessor('widex')
    if ratio > 0.75 and ratio < 0.9:
        imgProcessor('wide')
    if ratio < 1.6 and ratio > 1.1:
        imgProcessor('long')
    if ratio >= 1.6:
        imgProcessor('longx')
    if ratio == 1 or (ratio >= 0.9 and ratio <= 1.1):
        imgProcessor('square')
    new = open('end.png', 'rb')
    bot.send_photo(message.chat.id, new)


bot.infinity_polling()
