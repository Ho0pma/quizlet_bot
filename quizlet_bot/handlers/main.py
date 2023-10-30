from aiogram import Dispatcher
from handlers.user.main import register_user_handlers, register_user_callback_query_handlers
from handlers.other import register_other_handlers

def register_all_handlers(dp: Dispatcher) -> None:
    try:
        handlers = (
            register_user_handlers,
            register_user_callback_query_handlers,
            register_other_handlers,
        )
        for handler in handlers:
            handler(dp)
    except Exception as e:
        print(f"An error occurred in def register_all_handlers: {str(e)}")