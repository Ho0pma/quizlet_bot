from aiogram import Dispatcher
from aiogram.types import Message
from states import FSM
from texts.all_texts import Texts
from keyboards import reply

async def echo_main_menu(message: Message):
    try:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.echo_main_menu
        )
    except Exception as e:
        print(f"An error occurred in def echo_main_menu: {str(e)}")

async def echo_help(message: Message):
    try:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.echo_help,
            parse_mode='HTML',
            reply_markup=reply.get_kb_help()
        )
    except Exception as e:
        print(f"An error occurred in def echo_help: {str(e)}")

async def echo_not_photo(message: Message):
    try:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.echo_not_photo,
            parse_mode='HTML',
        )
    except Exception as e:
        print(f"An error occurred in def echo_not_photo: {str(e)}")


async def echo_got_file(message: Message):
    try:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.echo_got_file,
            parse_mode='HTML',
        )
    except Exception as e:
        print(f"An error occurred in def echo_got_file: {str(e)}")

async def echo_answer(message: Message):
    try:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.echo_answer,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"An error occurred in def echo_answer: {str(e)}")

async def echo_next(message: Message):
    try:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.echo_next,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"An error occurred in def echo_next: {str(e)}")


async def echo_callback(message: Message):
    try:
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.echo_callback,
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"An error occurred in def echo_callback: {str(e)}")

def register_other_handlers(dp: Dispatcher) -> None:
    try:
        dp.register_message_handler(echo_main_menu, state=FSM.main_menu)
        dp.register_message_handler(echo_help)
        dp.register_message_handler(echo_not_photo, state=FSM.get_photo)
        dp.register_message_handler(echo_got_file, content_types=['document'], state=FSM.get_photo)
        dp.register_message_handler(echo_answer, state=FSM.answer)
        dp.register_message_handler(echo_next, state=FSM.next_word)
        dp.register_message_handler(
            echo_callback, state=[
                FSM.after_create,
                FSM.after_shared,
                FSM.decision_to_upload_photo,
                FSM.decision_what_train,
                FSM.no_words,
                FSM.after_delete,
                FSM.after_swag
            ]
        )
    except Exception as e:
        print(f"An error occurred in def register_other_handlers: {str(e)}")


