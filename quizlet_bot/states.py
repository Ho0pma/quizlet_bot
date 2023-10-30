from aiogram.dispatcher.filters.state import StatesGroup, State

class FSM(StatesGroup):
    main_menu = State()
    get_word = State()
    get_desc = State()
    get_photo = State()
    get_help = State()
    after_create = State()
    after_shared = State()
    decision_to_upload_photo = State()
    train = State()
    next_word = State()
    answer = State()
    decision_what_train = State()
    get_author = State()
    no_words = State()
    delete_input = State()
    after_delete = State()
    after_swag = State()
    leave_comment = State()
