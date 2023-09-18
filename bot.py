import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.callback_data import CallbackData
from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from celery import shared_task
from dotenv import dotenv_values
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from threading import Timer

import message_text
from connect_db import DataUser
from keyboards import keyboard_back

env_vars = dotenv_values('.env')

bot = Bot(token=env_vars['BOT_TOKEN'])
dp = Dispatcher()


class CallbackMess(CallbackData, prefix="mess"):
    message_data: str
    save_button: str
    video: str
    photo: str


class Form(StatesGroup):
    new_mess = State()
    date_mess = State()


def task_delay():
    send_mess.delay()


@dp.message(Form.date_mess)
async def date(message: types.Message, state: FSMContext):
    from datetime import datetime

    current_datetime = datetime.now()
    data_now = int(current_datetime.timestamp())
    date_mess = int(datetime.strptime(message.text.lower(), '%Y-%m-%d %H:%M:%S').timestamp())
    await message.answer(text=message_text.date_save + str(date_mess-data_now), reply_markup=keyboard_back)
    time_job = Timer(date_mess-data_now, task_delay)
    time_job.start()
    await state.clear()


@dp.message(Form.new_mess)
async def save(message: types.Message, state: FSMContext):
    from keyboards import back, change_message

    if message.photo is not None:
        photo_path = 'photos/' + message.photo[-1].file_unique_id + '.png'
        await message.photo[-1].download(destination_file=photo_path)
        save_but = InlineKeyboardButton(
            text=message_text.save,
            callback_data=CallbackMess(message_data=message.text.lower(), save_button='save', video='nan',
                                       photo=photo_path).pack())
        keyboard_new = InlineKeyboardMarkup(
            inline_keyboard=[[save_but], [change_message], [back]])

        await message.answer(text=message_text.new_mess_end + message.text.lower(),
                             reply_markup=keyboard_new)

    elif message.video is not None:
        video_path = 'video/' + message.video.file_id + '.mp4'
        file = await bot.get_file(message.video.file_id)
        await bot.download_file(file.file_path, video_path)
        save_but = InlineKeyboardButton(
            text=message_text.save,
            callback_data=CallbackMess(message_data=message.text.lower(), save_button='save', video=file,
                                       photo='nan').pack())
        keyboard_new = InlineKeyboardMarkup(
            inline_keyboard=[[save_but], [change_message], [back]])

        await message.answer(text=message_text.new_mess_end+'hgfjghjfg' + message.text.lower(),
                             reply_markup=keyboard_new)

    else:
        save_but = InlineKeyboardButton(
            text=message_text.save,
            callback_data=CallbackMess(message_data=message.text.lower(), save_button='save', video='nan',
                                       photo='nan').pack())
        keyboard_new = InlineKeyboardMarkup(
            inline_keyboard=[[save_but], [change_message], [back]])

        await message.answer(text=message_text.new_mess_end + message.text.lower(),
                             reply_markup=keyboard_new)
    await state.clear()


@dp.callback_query(CallbackMess.filter(F.save_button == "save"))
async def process_button_save(callback: CallbackQuery, callback_data: CallbackMess):
    from keyboards import keyboard_start

    new_text = DataUser.create(chat_id=callback.message.chat.id, message=callback_data.message_data, video_mess=callback_data.video, img_mess=callback_data.photo)
    await callback.message.answer(text=message_text.save_mess,
                                  reply_markup=keyboard_start)
    await callback.answer()


@dp.callback_query(F.data == 'button_bask')
async def process_button_back(callback: CallbackQuery):
    from keyboards import keyboard_start

    await callback.message.answer(text=message_text.start_message_admin,
                                  reply_markup=keyboard_start)
    await callback.answer()


@dp.callback_query(F.data == 'button_new_message')
async def process_button_new(callback: CallbackQuery, state: FSMContext):
    from keyboards import keyboard_back

    await callback.message.answer(text=message_text.new_mode,
                                  reply_markup=keyboard_back)
    await state.set_state(Form.new_mess)


@dp.callback_query(F.data == 'button_change_message')
async def process_button_change(callback: CallbackQuery, state: FSMContext):
    from keyboards import keyboard_back

    mess = DataUser.select().where(DataUser.chat_id == env_vars['ID_ADMIN']).get().message

    if mess is not None:
        await callback.message.answer(text=message_text.old_mess + mess,
                                      reply_markup=keyboard_back)
    else:
        await callback.message.answer(text=message_text.not_mess)
    await state.set_state(Form.new_mess)


@shared_task
async def send_mess():
    if DataUser.select().where(DataUser.chat_id == env_vars['ID_ADMIN']).get().img_mess is not None \
            and DataUser.select().where(DataUser.chat_id == env_vars['ID_ADMIN']).get().img_mess != "nan":
        photo = DataUser.select().where(DataUser.chat_id == env_vars['ID_ADMIN']).get().img_mess
        for user in DataUser.select():
            await bot.send_photo(user.chat_id, photo, caption=DataUser.select().where(
                DataUser.chat_id == env_vars['ID_ADMIN']).get().message)
    elif DataUser.select().where(DataUser.chat_id == env_vars['ID_ADMIN']).get().video_mess is not None \
            and DataUser.select().where(DataUser.chat_id == env_vars['ID_ADMIN']).get().video_mess != "nan":
        video = DataUser.select().where(DataUser.chat_id == env_vars['ID_ADMIN']).get().video_mess
        for user in DataUser.select():
            await bot.send_video(user.chat_id, video, caption=DataUser.select().where(
                DataUser.chat_id == env_vars['ID_ADMIN']).get().message)
    else:
        for user in DataUser.select():
            await bot.send_message(user.chat_id, DataUser.select().where(DataUser.chat_id == env_vars['ID_ADMIN']).get().message)


@dp.callback_query(F.data == 'button_newsletter')
async def process_button_newsletter(callback: CallbackQuery):
    await send_mess()


@dp.callback_query(F.data == 'button_schedule_a_newsletter')
async def process_button_schedule_a_newsletter(callback: CallbackQuery, state: FSMContext):
    from keyboards import keyboard_back
    await callback.message.answer(text=message_text.date_mess,
                                  reply_markup=keyboard_back)
    await state.set_state(Form.date_mess)


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    try:
        DataUser.get(DataUser.chat_id==message.chat.id)
    except DataUser.DoesNotExist:
        new_user = DataUser(chat_id=message.chat.id)
        new_user.save()
    if str(message.from_user.id) == env_vars['ID_ADMIN']:
        from keyboards import keyboard_start
        await message.answer(message_text.start_message_admin, reply_markup=keyboard_start)

    else:
        await message.answer(message_text.start_message)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
