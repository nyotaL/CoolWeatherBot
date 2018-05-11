from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import mykeys

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

import poems

import image_search
import messages
import weather_teller


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(messages.HELLO)

def help(bot, update):
    update.message.reply_text(messages.HELP)

def forcast(bot, update):
    forecaster = weather_teller.Forecaster()
    weather_condition, city, ans_message = forecaster.forecast(update.message.text)

    if weather_condition == -1:
        update.message.reply_text(messages.INVALID_INPUT)
        return

    update.message.reply_text(ans_message)

    image_finder = image_search.ImageFinder()
    image_finder.set_params(weather_condition, city)
    picture_url = image_finder.search()

    picture_index = 0
    picture_send = False
    while not picture_send and picture_index < len(picture_url):
        try:
            bot.send_photo(chat_id=update.message.chat.id, photo=picture_url[picture_index]['contentUrl'])
            picture_send = True
        except Exception:
            picture_index += 1

        if picture_send:
            update.message.reply_text(poems.poems[weather_condition])
        else:
            update.message.reply_text(messages.IMAGE_PROBLEMS)

def talk(bot, update):
    update.message.reply_text('Хотите прогноз?')

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(mykeys.TOKEN, request_kwargs = mykeys.proxy)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("forcast", talk))
    dp.add_handler(MessageHandler(Filters.text, forcast))

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()
