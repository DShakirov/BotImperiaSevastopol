import datetime
import logging
import os

import telegram
from django.utils import timezone
from bot.handlers import commands
from bot.handlers import static_text as st
from bot.handlers import manage_data as md
from bot.handlers import keyboard_utils as kb
from bot.handlers.utils import handler_logging
from bot.models import User, Post, Message
from bot.tasks import broadcast_message
from bot.utils import convert_2_user_time, extract_user_data_from_update, get_chat_id, get_user_message, get_user_photo
from imperiasevastopol_bot.settings import BASE_DIR

logger = logging.getLogger('default')

"""@handler_logging()
def btn1_hnd(update, context):
    user_id = extract_user_data_from_update(update)['user_id']

    markup = kb.make_btn_keyboard()
    msg = f'{st.pressed}1'

    context.bot.edit_message_text(
        text=msg,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        reply_markup=markup,
        parse_mode=telegram.ParseMode.MARKDOWN,
    )"""


@handler_logging()
def about_us(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    posts = Post.objects.filter(category__slug='o-nas')[:5]
    markup = kb.make_btn_keyboard()
    for post in posts:
        msg = f'<b>{post.title}</b>\n{post.content}'
        try:
            img = post.image.url
        except:
            img = None
        if img:
            context.bot.send_photo(
                photo=open((str(BASE_DIR) + img), 'rb'),
                chat_id=user_id,
                parse_mode=telegram.ParseMode.MARKDOWN
            )
        context.bot.send_message(text=msg, chat_id=user_id, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(text='На главную', chat_id=user_id, reply_markup=markup)


@handler_logging()
def project_3d(update, context):
    posts = Post.objects.filter(category__slug='3d-proekt')[:5]
    user_id = extract_user_data_from_update(update)['user_id']
    markup = kb.make_btn_keyboard()
    for post in posts:
        msg = f'<b>{post.title}</b>\n{post.content}'
        try:
            img = post.image.url
        except:
            img = None
        if img:
            context.bot.send_photo(
                photo=open((str(BASE_DIR) + img), 'rb'),
                chat_id=user_id,
            )
        context.bot.send_message(text=msg, chat_id=user_id, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(text='На главную', chat_id=user_id, reply_markup=markup)


@handler_logging()
def promotions(update, context):
    posts = Post.objects.filter(category__slug='akcii')[:10]
    user_id = extract_user_data_from_update(update)['user_id']
    markup = kb.make_btn_keyboard()
    for post in posts:
        msg = f'<b>{post.title}</b>\n{post.content}'
        try:
            img = post.image.url
        except:
            img = None
        if img:
            context.bot.send_photo(
                photo=open((str(BASE_DIR) + img), 'rb'),
                chat_id=user_id,
            )
        context.bot.send_message(text=msg, chat_id=user_id, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(text='На главную', chat_id=user_id, reply_markup=markup)

@handler_logging()
def week_sales(update, context):
    posts = Post.objects.filter(category__slug='tovar-nedeli')[:10]
    user_id = extract_user_data_from_update(update)['user_id']
    markup = kb.make_btn_keyboard()
    for post in posts:
        msg = f'<b>{post.title}</b>\n{post.content}'
        try:
            img = post.image.url
        except:
            img = None
        if img:
            context.bot.send_photo(
                photo=open((str(BASE_DIR) + img), 'rb'),
                chat_id=user_id,
            )
        context.bot.send_message(text=msg, chat_id=user_id, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(text='На главную', chat_id=user_id, reply_markup=markup)

@handler_logging()
def faq(update, context):
    posts = Post.objects.filter(category__slug='vopros-otvet')[:10]
    user_id = extract_user_data_from_update(update)['user_id']
    markup = kb.make_btn_keyboard()
    for post in posts:
        msg = f'<b>{post.title}</b>\n{post.content}'
        try:
            img = post.image.url
        except:
            img = None
        if img:
            context.bot.send_photo(
                photo=open((str(BASE_DIR) + img), 'rb'),
                chat_id=user_id,
            )
        context.bot.send_message(text=msg, chat_id=user_id, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(text='На главную', chat_id=user_id, reply_markup=markup)

@handler_logging()
def location(update, context):
    posts = Post.objects.filter(category__slug='mestopolozhenie')[:2]
    user_id = extract_user_data_from_update(update)['user_id']
    markup = kb.make_btn_keyboard()
    for post in posts:
        msg = f'<b>{post.title}</b>\n{post.content}'
        try:
            img = post.image.url
        except:
            img = None
        if img:
            context.bot.send_photo(
                photo=open((str(BASE_DIR) + img), 'rb'),
                chat_id=user_id,
            )
        context.bot.send_message(text=msg, chat_id=user_id, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(text='На главную', chat_id=user_id, reply_markup=markup)

@handler_logging()
def contacts(update, context):
    posts = Post.objects.filter(category__slug='kontakty')[:3]
    user_id = extract_user_data_from_update(update)['user_id']
    markup = kb.make_btn_keyboard()
    for post in posts:
        msg = f'<b>{post.title}</b>\n{post.content}'
        try:
            img = post.image.url
        except:
            img = None
        if img:
            context.bot.send_photo(
                photo=open((str(BASE_DIR) + img), 'rb'),
                chat_id=user_id,
            )
        context.bot.send_message(text=msg, chat_id=user_id, parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(text='На главную', chat_id=user_id, reply_markup=markup)

@handler_logging()
def back_to_main_menu_handler(update, context):  # callback_data: BUTTON_BACK_IN_PLACE variable from manage_data.py
    user, created = User.get_user_and_created(update, context)

    payload = context.args[0] if context.args else user.deep_link  # if empty payload, check what was stored in DB
    text = st.welcome

    user_id = extract_user_data_from_update(update)['user_id']
    context.bot.edit_message_text(
        chat_id=user_id,
        text=text,
        message_id=update.callback_query.message.message_id,
        reply_markup=kb.make_keyboard_for_start_command(),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


@handler_logging()
def secret_level(update, context):  # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = "Congratulations! You've opened a secret room👁‍🗨. There is some information for you:\n" \
           "*Users*: {user_count}\n" \
           "*24h active*: {active_24}".format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN
    )

@handler_logging()
def user_message(update, context):
    #записываем сообщение в БД
    data = get_user_message(update)
    text = data['text']
    user_id = data['user_id']
    message_id = data['message_id']
    Message.objects.create(text=text, user=User.objects.get(user_id=user_id))
    #пересылаем сообщение администратору
    admin_ids = User.objects.filter(is_admin=True).values_list('user_id', flat=True)
    if len(admin_ids) > 0 and user_id not in admin_ids:
        for admin_id in admin_ids:
            context.bot.forward_message(chat_id=admin_id, from_chat_id=user_id, message_id=message_id)
    #Все отработало. Возвращаемся на главную
    markup = kb.make_btn_keyboard()
    context.bot.send_message(text='Спасибо за обратную связь.\n Вернуться на главную.', chat_id=user_id, reply_markup=markup)

@handler_logging()
def user_caption_and_photo(update, context):
    data = get_user_photo(update)
    photo = context.bot.get_file(file_id=data['file_id']).download(custom_path=f"images/{data['file_id']}.jpg")
    text = data['text']
    user_id = data['user_id']
    message_id = data['message_id']
    Message.objects.create(text=text, user=User.objects.get(user_id=user_id), image=photo)

    admin_ids = User.objects.filter(is_admin=True).values_list('user_id', flat=True)
    if len(admin_ids) > 0 and user_id not in admin_ids:
        for admin_id in admin_ids:
            context.bot.forward_message(chat_id=admin_id, from_chat_id=user_id, message_id=message_id)

    markup = kb.make_btn_keyboard()
    context.bot.send_message(text='Спасибо за обратную связь.\n Вернуться на главную.', chat_id=user_id, reply_markup=markup)

def broadcast_decision_handler(update,
                               context):  # callback_data: CONFIRM_DECLINE_BROADCAST variable from manage_data.py
    """ Entered /broadcast <some_text>.
        Shows text in Markdown style with two buttons:
        Confirm and Decline
    """
    broadcast_decision = update.callback_query.data[len(md.CONFIRM_DECLINE_BROADCAST):]
    entities_for_celery = update.callback_query.message.to_dict().get('entities')
    entities = update.callback_query.message.entities
    text = update.callback_query.message.text
    if broadcast_decision == md.CONFIRM_BROADCAST:
        admin_text = st.msg_sent,
        user_ids = list(User.objects.all().values_list('user_id', flat=True))
        broadcast_message.delay(user_ids=user_ids, message=text, entities=entities_for_celery)
    else:
        admin_text = text

    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        entities=None if broadcast_decision == md.CONFIRM_BROADCAST else entities
    )
