from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from texts.all_texts import Texts

def get_inl_kb_after_create():
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text=Texts.add_to_shared, callback_data='/shared'),
        InlineKeyboardButton(text=Texts.another_one, callback_data='/create'),
        InlineKeyboardButton(text=Texts.go_to_the_menu, callback_data='/main')
    ]
    kb.add(buttons[1]).add(buttons[0]).add(buttons[2])
    return kb

def get_inl_kb_for_decision_to_upload_photo():
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text='Yes', callback_data='/get_photo'),
        InlineKeyboardButton(text='No', callback_data='/no_get_photo'),
    ]
    kb.add(*buttons)
    return kb

def get_inl_kb_after_shared():
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text=Texts.go_to_the_menu, callback_data='/main'),
        InlineKeyboardButton(text=Texts.another_one, callback_data='/create')
    ]
    kb.add(buttons[0]).add(buttons[1])
    return kb

def get_inl_kb_decision_what_train():
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text='personal', callback_data='/personal'),
        InlineKeyboardButton(text='shared', callback_data='/shared'),
    ]
    kb.add(*buttons)
    return kb

def get_inl_kb_when_user_dont_have_any_words():
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text=Texts.go_to_the_menu, callback_data='/main'),
        InlineKeyboardButton(text=Texts.create_when_no_words, callback_data='/create')
    ]
    kb.add(buttons[0]).add(buttons[1])
    return kb

def get_inl_kb_after_delete_word():
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text=Texts.go_to_the_menu, callback_data='/main'),
        InlineKeyboardButton(text=Texts.another_one, callback_data='/delete')
    ]
    kb.add(buttons[0]).add(buttons[1])
    return kb

def get_inl_kb_swag():
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text=Texts.go_to_the_menu, callback_data='/main'),
        InlineKeyboardButton(text=Texts.comment, callback_data='/comment'),
    ]
    kb.add(buttons[1]).add(buttons[0])
    return kb

def get_inl_kb_after_leave_comment():
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text=Texts.go_to_the_menu, callback_data='/main'),
        InlineKeyboardButton(text=Texts.another_one, callback_data='/comment'),
    ]
    kb.add(buttons[0]).add(buttons[1])
    return kb


