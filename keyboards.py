from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import message_text
new_message = InlineKeyboardButton(
    text=message_text.new_message,
    callback_data='button_new_message')

change_message = InlineKeyboardButton(
    text=message_text.change_message,
    callback_data='button_change_message')

back = InlineKeyboardButton(
    text=message_text.back,
    callback_data='button_bask')

save = InlineKeyboardButton(
    text=message_text.save,
    callback_data='button_save')

newsletter = InlineKeyboardButton(
    text=message_text.newsletter_mess,
    callback_data='button_newsletter')

schedule_a_newsletter = InlineKeyboardButton(
    text=message_text.schedule_a_newsletter_mess,
    callback_data='button_schedule_a_newsletter')

keyboard_start = InlineKeyboardMarkup(
    inline_keyboard=[[newsletter],
                     [new_message],
                     [change_message],
                     [schedule_a_newsletter]])

keyboard_mess = InlineKeyboardMarkup(
    inline_keyboard=[[save],
                     [back]])

keyboard_back = InlineKeyboardMarkup(
    inline_keyboard=[[back]])

keyboard_new = InlineKeyboardMarkup(
    inline_keyboard=[[save],
                     [change_message],
                     [back]])
