"""Telegram event handlers."""

import telegram

from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler, PollAnswerHandler,
)

from celery import shared_task  # event processing in async mode

from imperiasevastopol_bot.settings import TELEGRAM_TOKEN

from bot.handlers import admin, commands, files
from bot.handlers.commands import broadcast_command_with_message
from bot.handlers import handlers as hnd
from bot.handlers import manage_data as md
from bot.handlers.static_text import broadcast_command


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """

    dp.add_handler(CommandHandler("start", commands.command_start))

    # admin commands
    dp.add_handler(CommandHandler("admin", admin.admin))
    #dp.add_handler(CommandHandler("stats", admin.stats))

    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))

    # base buttons
    dp.add_handler(CallbackQueryHandler(hnd.about_us, pattern=f'^{md.ABOUT_US}'))
    dp.add_handler(CallbackQueryHandler(hnd.project_3d, pattern=f'^{md.PROJECT}'))
    dp.add_handler(CallbackQueryHandler(hnd.promotions, pattern=f'^{md.PROMOTIONS}'))
    dp.add_handler(CallbackQueryHandler(hnd.week_sales, pattern=f'^{md.WEEK_SALES}'))
    dp.add_handler(CallbackQueryHandler(hnd.faq, pattern=f'^{md.FAQ}'))
    dp.add_handler(CallbackQueryHandler(hnd.location, pattern=f'^{md.LOCATION}'))
    dp.add_handler(CallbackQueryHandler(hnd.contacts, pattern=f'^{md.CONTACTS}'))
    #dp.add_handler(CallbackQueryHandler(hnd.btn3_hnd, pattern=f'^{md.BTN_3}'))

    dp.add_handler(CallbackQueryHandler(hnd.back_to_main_menu_handler, pattern=f'^{md.BUTTON_BACK_IN_PLACE}'))

    dp.add_handler(CallbackQueryHandler(hnd.secret_level, pattern=f"^{md.SECRET_LEVEL_BUTTON}"))

    dp.add_handler(MessageHandler(Filters.regex(rf'^{broadcast_command} .*'), broadcast_command_with_message))
    dp.add_handler(CallbackQueryHandler(hnd.broadcast_decision_handler, pattern=f"^{md.CONFIRM_DECLINE_BROADCAST}"))
    dp.add_handler(MessageHandler(Filters.text, callback=hnd.user_message))
    dp.add_handler(MessageHandler(Filters.caption, callback=hnd.user_caption_and_photo))
    dp.add_handler(MessageHandler(Filters.photo, callback=hnd.user_caption_and_photo))

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling(timeout=123)
    updater.idle()


@shared_task(ignore_result=True)
def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)


# Global variable - best way I found to init Telegram bot
bot = telegram.Bot(TELEGRAM_TOKEN)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=0, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]