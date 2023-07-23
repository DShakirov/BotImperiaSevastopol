import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imperiasevastopol_bot.settings')
django.setup()

from bot.handlers.dispatcher import run_pooling

if __name__ == "__main__":
    run_pooling()