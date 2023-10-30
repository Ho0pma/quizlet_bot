from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from misc.env import TgKeys
from handlers.main import register_all_handlers

async def __on_start_up(dp: Dispatcher) -> None:
    try:
        print('The bot has started 0_0')
        register_all_handlers(dp)
    except Exception as e:
        print(f"An error occurred in def __on_start_up: {str(e)}")


def start_bot():
    try:
        bot = Bot(token=TgKeys.TOKEN)
        dp = Dispatcher(bot, storage=MemoryStorage())
        executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
    except Exception as e:
        print(f"An error occurred in def start_bot: {str(e)}")