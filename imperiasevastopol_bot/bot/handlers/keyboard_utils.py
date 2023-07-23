from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.handlers import manage_data as md
from bot.handlers import static_text as st


def make_btn_keyboard():
    buttons = [
        [
            InlineKeyboardButton(st.go_back, callback_data=f'{md.BUTTON_BACK_IN_PLACE}'),
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def make_keyboard_for_start_command():
    buttons = [
        [
            InlineKeyboardButton(st.about_us, callback_data=f'{md.ABOUT_US}'),
        ],
        [
            InlineKeyboardButton(st.week_sales, callback_data=f'{md.WEEK_SALES}'),            
            InlineKeyboardButton(st.promotions, callback_data=f'{md.PROMOTIONS}'),
        ],
        [
            InlineKeyboardButton(st.project, callback_data=f'{md.PROJECT}'),
        ],
        [
            InlineKeyboardButton(st.faq, callback_data=f'{md.FAQ}'),
            InlineKeyboardButton(st.location, callback_data=f'{md.LOCATION}'),
        ],
        [
            InlineKeyboardButton(st.contacts, callback_data=f'{md.CONTACTS}')
        ],
    ]

    return InlineKeyboardMarkup(buttons)


def keyboard_confirm_decline_broadcasting():
    buttons = [[
        InlineKeyboardButton(st.confirm_broadcast, callback_data=f'{md.CONFIRM_DECLINE_BROADCAST}{md.CONFIRM_BROADCAST}'),
        InlineKeyboardButton(st.decline_broadcast, callback_data=f'{md.CONFIRM_DECLINE_BROADCAST}{md.DECLINE_BROADCAST}')
    ]]

    return InlineKeyboardMarkup(buttons)