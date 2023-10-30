from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def get_kb_start():
    button = KeyboardButton('/menu')
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(button)
    return kb

def get_kb_back_to_menu():
    button = KeyboardButton('/back_to_menu')
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(button)
    return kb

def get_kb_answer():
    buttons = [KeyboardButton('/back_to_menu'), KeyboardButton('/answer')]
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*buttons)
    return kb

def get_kb_next():
    buttons = [KeyboardButton('/back_to_menu'), KeyboardButton('/next')]
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*buttons)
    return kb

def get_kb_help():
    button = KeyboardButton('/help')
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(button)
    return kb

def get_kb_menu():
    buttons = [
        KeyboardButton('/create'),
        KeyboardButton('/train'),
        KeyboardButton('/count'),
        KeyboardButton('/delete'),
        KeyboardButton('/authors'),
        KeyboardButton('/swag')
    ]
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*buttons)
    return kb