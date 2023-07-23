import json
import logging
from django.views import View
from django.http import JsonResponse, HttpResponse
from telegram import Update

from bot.handlers.dispatcher import bot
from bot.handlers import dispatcher
from imperiasevastopol_bot.celery import app
from imperiasevastopol_bot.settings import DEBUG

from bot.handlers.dispatcher import process_telegram_event, TELEGRAM_BOT_USERNAME

logger = logging.getLogger(__name__)

BOT_URL = f"https://t.me/{TELEGRAM_BOT_USERNAME}"

def index(request):
    return HttpResponse('Все в порядке')

@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


#class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    #def post(self, request, *args, **kwargs):
        #process_telegram_event.delay(json.loads(request.body))


        # e.g. remove buttons
        #return JsonResponse({"ok": "POST request processed"})

    #def get(self, request, *args, **kwargs):  # for debug
        #return JsonResponse({"ok": "Get request processed. But nothing done"})