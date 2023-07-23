from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views
from .views import index

urlpatterns = [
    path('', index,),
    # TODO: make webhook more secure
    #path('super_secter_webhook/', csrf_exempt(views.TelegramBotWebhookView.as_view())),
]