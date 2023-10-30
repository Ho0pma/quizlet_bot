from emoji import emojize
from io import BytesIO
from random import choice
from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from states import FSM
# from misc.google_drive_connection import GD_con

from keyboards import inline, reply

from texts.all_texts import Texts
from database.methods import insert, get, delete


def random_emoji_after_create():
    """
    Возвращает случайно выбранное эмодзи из списка. Используется после создания карточки

    Returns:
        str: Случайно выбранное эмодзи.
    """
    try:
        animal_lst = [
            '👾', '💫', '👮‍♂️', '🤦‍♀️', '😶‍🌫️', '🐈‍⬛', '🤦', '👨‍💻', '👩‍💻', '👮‍♀️',
        ]
        return choice(animal_lst)
    except Exception as e:
        print(f"An error occurred in def random_emoji_after_create: {str(e)}")


def random_next_emoji():
    """
    Возвращает случайно выбранное эмодзи из списка. Используется перед выводом следующего слова.

    Returns:
        str: Случайно выбранное эмодзи.
    """
    try:
        animal_lst = [
            '🦉', '🐍', '🐦️', '🦭', '🐤', '🐔', '🌚', '🌝', '👠', '🧨'
        ]
        return choice(animal_lst)
    except Exception as e:
        print(f"An error occurred in def random_next_emoji: {str(e)}")


def random_item(data):
    """
    Возвращает случайно выбранный элемент из переданного списка или итерируемого объекта. Используется для получения
    рандомного слова из слов созданных пользователем.

    Args:
        data (list or iterable): Список или итерируемый объект.

    Returns:
        Any: Случайно выбранный элемент из переданного списка или итерируемого объекта.
    """
    try:
        return choice(data)
    except Exception as e:
        print(f"An error occurred in def random_item: {str(e)}")


def folder_check(photos_folder_id, folder_title):
    """
    Проверяет, существует ли папка с указанным названием в заданной папке на Google Диске.

    Args:
        photos_folder_id (str): Идентификатор папки на Google Диске = имени пользователя в Telegram
        folder_title (str): Название папки, которую нужно проверить.

    Returns:
        bool: True, если папка с указанным названием уже существует, иначе False.
    """
    try:
        # Получаем список файлов в указанной папке на Google Диске
        file_list = GD_con.drive.ListFile(
            {
                'q': f"'{photos_folder_id}' in parents and trashed=false"
            }
        ).GetList()

        # Проверяем каждый файл в списке
        for file in file_list:
            if file['title'] == folder_title:
                return True  # Папка существует
        return False  # Папка не найдена
    except Exception as e:
        print(f"An error occurred in def folder_check: {str(e)}")


def get_folder_id(folder_name):
    """
    Получает идентификатор папки на Google Диске по её названию.

    Args:
        folder_name (str): Название папки.

    Returns:
        str or None: Идентификатор найденной папки или None, если папка не найдена.
    """
    try:
        # Получаем список файлов в указанной папке на Google Диске
        file_list = GD_con.drive.ListFile(
            {
                'q': f"'{GD_con.main_folder_id}' in parents and trashed=false"
            }
        ).GetList()

        # Проверяем каждый файл в списке
        for file in file_list:
            if file['title'] == folder_name and file['mimeType'] == 'application/vnd.google-apps.folder':
                return file['id']
    except Exception as e:
        print(f"An error occurred in def get_folder_id: {str(e)}")


def filter_data(data):
    """
    Функция для фильтрации данных перед использованием в тренировке.

    Args:
        data (dict): Словарь данных из состояния конечного автомата.

    Returns:
        tuple: Кортеж из выбранного слова и обновленных данных.
    """
    try:
        # Выбираем случайное слово из списка неиспользованных и обновляем данные
        item = random_item(data=data['items_not_used'])
        data['items_not_used'] = [i for i in data['items_not_used'] if i != item]
        data['items_were_used'].append(item)
        data['item_in_progres'] = item
        return item, data
    except Exception as e:
        print(f"An error occurred in def filter_data: {str(e)}")


async def help_me_someone(message: Message):
    """
    Обработчик для команды /help. Используется в случае, если пользователь находится ни одном из стейтов и не видит
    главного меню перед глазами. Выведет меню.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Отправляем сообщение со списком команд и убираем клавиатуру
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.commands,
            parse_mode='HTML',
            reply_markup=reply.get_kb_menu()
        )

        # Устанавливаем состояние FSM в main_menu
        await FSM.main_menu.set()
    except Exception as e:
        print(f"An error occurred in def help_me_someone: {str(e)}")


async def back_to_menu(message: Message, state: FSMContext):
    """
    Обработчик для команды /back_to_menu.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Завершаем текущее состояние и отправляем сообщение об отмене действия
        await state.finish()
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.commands,
            parse_mode='HTML',
            reply_markup=reply.get_kb_menu()
        )

        # Устанавливаем состояние FSM в main_menu
        await FSM.main_menu.set()
    except Exception as e:
        print(f"An error occurred in def back_to_menu: {str(e)}")


async def start(message: Message):
    """
    Обработчик команды /start, инициализирует начальное состояние бота. Приветственное сообщение + кнопка /menu

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Отправляем приветственное сообщение и кнопку /menu
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.start,
            parse_mode='HTML',
            reply_markup=reply.get_kb_start()
        )
        # Проверяем наличие папки пользователя на Google Диске
        if not folder_check(photos_folder_id=GD_con.main_folder_id, folder_title=message.from_user.username):
            # Если папки нет, создаем новую
            new_folder = GD_con.drive.CreateFile(
                {
                    'title': message.from_user.username,
                    'parents': [{'id': GD_con.main_folder_id}],
                    'mimeType': 'application/vnd.google-apps.folder'
                }
            )
            new_folder.Upload()
            print('A new user has been created: {}'.format(message.from_user.username))

        # Устанавливаем состояние FSM в main_menu
        await FSM.main_menu.set()
    except Exception as e:
        print(f"An error occurred in def start: {str(e)}")


async def menu(message: Message):
    """
    Обработчик команды /menu для отображения меню с командами.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Отправляем сообщение с командами и убираем клавиатуру
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.commands,
            reply_markup=reply.get_kb_menu(),
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"An error occurred in def menu: {str(e)}")

async def create_card(message: Message) -> None:
    """
    Обработчик команды для создания новой карточки. Просит вести слово

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Отправляем запрос на ввод слова и добавляем клавиатуру для возврата в главное меню
        await message.answer(
            text=Texts.set_the_word,
            reply_markup=reply.get_kb_back_to_menu()
        )

        # Устанавливаем состояние FSM в get_word
        await FSM.get_word.set()
    except Exception as e:
        print(f"An error occurred in def create_card: {str(e)}")


async def get_word(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения введенного пользователем слова и просьбы ввести определение слова.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Сохраняем введенное слово в MemoryStorage
        async with state.proxy() as data:
            data['word'] = message.text

        # Запрашиваем описание и устанавливаем состояние FSM в get_desc
        await message.answer(
            text=Texts.set_the_decs
        )

        # Устанавливаем состояние FSM в get_desc
        await FSM.get_desc.set()
    except Exception as e:
        print(f"An error occurred in def get_word: {str(e)}")


async def get_desc(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения введенного пользователем описания и предложение добавить фото (инлайн клавиатура)

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Сохраняем введенное описание в MemoryStorage
        async with state.proxy() as data:
            data['desc'] = message.text

        # Задаем вопрос о загрузке фото и устанавливаем состояние FSM в decision_to_upload_photo
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.ask_to_set_the_photo,
            reply_markup=inline.get_inl_kb_for_decision_to_upload_photo()
        )

        # Устанавливаем состояние FSM в decision_to_upload_photo
        await FSM.decision_to_upload_photo.set()
    except Exception as e:
        print(f"An error occurred in def get_desc: {str(e)}")


async def get_photo(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения отправленного пользователем фото и загрузки его на Google Диск.

    Args:
        message (Message): Объект сообщения от пользователя с фото.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Получаем информацию о фото
        photo_file_id = message.photo[-1].file_id
        photo_info = await message.bot.get_file(
            file_id=photo_file_id
        )

        # Получаем идентификатор папки пользователя на Google Диске
        user_folder_id = get_folder_id(
            folder_name=message.from_user.username
        )

        # Загружаем фото на Google Диск
        photo_content = await message.bot.download_file(
            file_path=photo_info.file_path
        )
        gdrive_file = GD_con.drive.CreateFile(
            {
                'title': photo_file_id,
                'parents': [{'id': user_folder_id}]
            }
        )
        gdrive_file.content = BytesIO(
            photo_content.getvalue()
        )
        gdrive_file.Upload()

        # Сохраняем ссылку на фото в MemoryStorage
        async with state.proxy() as data:
            data['url'] = gdrive_file['alternateLink']
            print(f"File uploaded to Google Drive. URL: {data['url']}")

        # Отправляем сообщение об успешном создании с эмодзи и кнопками
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=emojize(string=random_emoji_after_create())
        )
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.done,
            parse_mode='HTML',
            reply_markup=inline.get_inl_kb_after_create()
        )

        # Устанавливаем состояние FSM в after_create
        await FSM.after_create.set()

    except Exception as e:
        print(f"An error occurred in def get_photo: {str(e)}")


async def start_train(message: Message) -> None:
    """
    Обработчик для команды /train. Инлайн клавиатура с выбором shared / personal

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Отправляем сообщение с выбором типа тренировки и устанавливаем состояние FSM в decision_what_train
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.choose_what_train,
            reply_markup=inline.get_inl_kb_decision_what_train()
        )

        # Устанавливаем состояние FSM в decision_what_train
        await FSM.decision_what_train.set()
    except Exception as e:
        print(f"An error occurred in start_train: {str(e)}")


async def answer(message: Message, state: FSMContext) -> None:
    """
    Обработчик для команды /answer.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Получаем данные из MemoryStorage и отправляем ответ пользователю
        data = await state.get_data()
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.answer.format(data['item_in_progres'][1]),
            parse_mode='HTML',
            reply_markup=reply.get_kb_next()
        )

        # Устанавливаем состояние FSM в next_word
        await FSM.next_word.set()
    except Exception as e:
        print(f"An error occurred in def answer: {str(e)}")


async def next_word(message: Message, state: FSMContext) -> None:
    """
    Обработчик для команды /next. Выводит следующий вопрос.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Получаем данные из MemoryStorage и выбираем следующее слово для тренировки
        async with state.proxy() as data:
            if not data['items_not_used']:
                data['items_not_used'], data['items_were_used'] = data['items_were_used'], data['items_not_used']
                item, data = filter_data(data)
            else:
                item, data = filter_data(data)

        # Отправляем эмодзи и следующее слово
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=emojize(string=random_next_emoji())
        )
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.question.format(item[0]),
            parse_mode='HTML',
            reply_markup=reply.get_kb_answer()
        )

        # Если у слова есть фото, отправляем его пользователю
        if data['item_in_progres'][2] != '0':
            await send_photo(message=message, data=data)

        # Устанавливаем состояние FSM в answer
        await FSM.answer.set()
    except Exception as e:
        print(f"An error occurred in def next_word: {str(e)}")


async def send_photo(message, data):
    """
    Отправляет фото из Google Диска пользователю.

    Args:
        message (Message): Объект сообщения от пользователя.
        data (dict): Словарь данных из состояния конечного автомата.
    """
    try:
        # Получаем URL фото из данных и извлекаем из него идентификатор файла
        url = data['item_in_progres'][2]
        start_index = url.find('/d/') + 3
        end_index = url.find('/view')
        file_id = url[start_index:end_index]

        # Создаем объект файла по его идентификатору
        file = GD_con.drive.CreateFile(
            {
                'id': file_id
            }
        )

        # Получаем содержимое файла и отправляем его пользователю в виде фото
        file.FetchContent()
        await message.answer_photo(
            photo=file.content
        )
    except Exception as e:
        print(f"An error occurred in def send_photo: {str(e)}")


async def count_words(message: Message) -> None:
    """
    Обработчик для команды /count. Выводит кол-во слов пользователя из personal и shared

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Получаем количество персональных и общих слов пользователя из базы данных
        count_not_shared = get.select_count_words_by_user_not_shared(username=message.from_user.username)
        count_shared = get.select_count_words_by_user_shared(username=message.from_user.username)

        # Отправляем пользователю информацию о количестве его слов
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.statistics.format(
                count_not_shared + count_shared,
                count_not_shared,
                count_shared
            ),
            parse_mode='HTML'
        )
    except Exception as e:
        print(f"An error occurred in def count_words: {str(e)}")


async def after_decision_what_train(message: Message, all_items, state: FSMContext):
    """
    Обработчик для дальнейших действий после выбора типа тренировки.

    Args:
        message (Message): Объект сообщения от пользователя.
        all_items (list): Список всех слов для тренировки.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Отправляем эмодзи и выбираем случайное слово для тренировки
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=emojize(string=random_next_emoji())
        )
        item = random_item(data=all_items)

        # Обновляем данные в MemoryStorage конечного автомата
        async with state.proxy() as data:
            data['items_not_used'] = [i for i in all_items if i != item]
            data['items_were_used'] = [item]
            data['item_in_progres'] = item

        # Отправляем пользователю слово и, если есть, фото
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.question.format(item[0]),
            parse_mode='HTML',
            reply_markup=reply.get_kb_answer()
        )
        if data['item_in_progres'][2] != '0':
            await send_photo(message=message, data=data)

        # Устанавливаем состояние FSM в answer
        await FSM.answer.set()
    except Exception as e:
        print(f"An error occurred in def after_decision_what_train: {str(e)}")


async def authors(message: Message) -> None:
    """
    Обработчик для команды /authors. Выводит авторов и список слов, что они создали

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Получаем список авторов и их слов из базы данных
        authors_lst = get.select_authors_and_words()
        if authors_lst:
            # Создаем словарь для группировки слов по авторам
            result_dict = {}
            for key, value in authors_lst:
                if key in result_dict:
                    result_dict[key].append(value)
                else:
                    result_dict[key] = [value]

            # Формируем строку с информацией об авторах и их словах
            result_string = ''
            for key, value in result_dict.items():
                formatted_value = ', '.join([f"'{v}'" for v in value])
                result_string += f"<i><b>{key}:</b></i> [{formatted_value}]\n"

            # Отправляем пользователю информацию об авторах
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=Texts.authors + result_string,
                parse_mode='HTML'
            )
        else:
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=Texts.no_words_in_shared,
                parse_mode='HTML'
            )
    except Exception as e:
        print(f"An error occurred in def authors: {str(e)}")


async def delete_photo_from_gd(url: str):
    """
    Удаляет фото из Google Диска по его URL.

    Args:
        url (str): URL фото на Google Диске.
    """
    try:
        if url != '0':
            try:
                # Извлекаем идентификатор файла из URL
                start_index = url.find('/d/') + 3
                end_index = url.find('/view')
                file_id = url[start_index:end_index]

                # Создаем объект файла по его идентификатору и удаляем его
                file = GD_con.drive.CreateFile({'id': file_id})
                file.Delete()
                print(f"Файл с ID {file_id} успешно удален.")
            except Exception as e:
                print(f"Произошла ошибка при удалении файла: {str(e)}")
    except Exception as e:
        print(f"An error occurred in def delete_photo_from_gd: {str(e)}")


async def delete_start(message: Message) -> None:
    """
    Обработчик для команды /delete. Удаляем по слову из бд.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Отправляем сообщение с просьбой отправить слово для удаления
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.delete
        )

        # Устанавливаем состояние FSM в delete_input
        await FSM.delete_input.set()
    except Exception as e:
        print(f"An error occurred in def delete_start: {str(e)}")


async def delete_input(message: Message) -> None:
    """
    Обработчик для ввода слова, которое пользователь хочет удалить. + удаление из Google Диска

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Получаем введенное пользователем слово и пытаемся удалить его из базы данных
        input_message = message.text
        delete_result = delete.delete_word_from_main_library(
            username=message.from_user.username,
            word=input_message
        )

        # Если удаление успешно, удаляем фото из Google Диска и переходим к следующему шагу
        if delete_result:
            await delete_photo_from_gd(url=delete_result[3])
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=Texts.done,
                parse_mode='HTML',
                reply_markup=inline.get_inl_kb_after_delete_word()
            )

            # Устанавливаем состояние FSM в after_delete
            await FSM.after_delete.set()
        else:
            # Если слово не найдено, отправляем сообщение об ошибке и просим ввести еще раз
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=Texts.word_not_found,
                parse_mode='HTML',
                reply_markup=reply.get_kb_back_to_menu()
            )

            # Устанавливаем состояние FSM в delete_input
            await FSM.delete_input.set()
    except Exception as e:
        print(f"An error occurred in def delete_input: {str(e)}")


async def swag(message: Message) -> None:
    """
    Обработчик для вывода комментариев.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Приветственное сообщение
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.swag,
            parse_mode='HTML',
            reply_markup=ReplyKeyboardRemove()
        )

        #Забираем комменты из бд и формируем из них строку
        comments = get.select_from_swag_comments()
        if comments:
            result_string = ''
            for item in comments:
                result_string += f"<i><b>{item[0]}:</b></i> {item[1]}\n"

            # выводим полученную строку пользователю + добавляем клаву
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=result_string,
                parse_mode='HTML',
                reply_markup=inline.get_inl_kb_swag()
            )

            # Устанавливаем состояние FSM в after_swag
            await FSM.after_swag.set()
        else:
            # Выводим сообщение о том, что нет записей
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=Texts.no_comments,
                parse_mode='HTML',
                reply_markup=inline.get_inl_kb_swag()
            )

            # Устанавливаем состояние FSM в after_swag
            await FSM.after_swag.set()
    except Exception as e:
        print(f"An error occurred in def swag: {str(e)}")


async def leave_comment_in_db(message: Message) -> None:
    """
    Функция для добавления полученного комментария в бд + предложения о вводе нового или возврата в меню.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    try:
        # Вставляем коммент в таблицу
        insert.insert_into_swag(
            username=message.from_user.username,
            comment=message.text
        )
        # Сообщаем, что все гут, предлагаем выбор с помощью инлайн клавиатуры
        await message.bot.send_message(
            chat_id=message.chat.id,
            text=Texts.done,
            parse_mode='HTML',
            reply_markup=inline.get_inl_kb_after_leave_comment()
        )

        # Устанавливаем состояние FSM в after_swag
        await FSM.after_swag.set()

    except Exception as e:
        print(f"An error occurred in def leave_comment: {str(e)}")

async def callback_inl_kb_after_swag(call: CallbackQuery):
    """
    Обработчик для реагирования на нажатие кнопок в меню решения об написании комментария.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
    """
    try:
        # Данные полученные с inline-кнопок
        callback_data = call.data

        # Обработка кнопки '/create'
        if callback_data == '/comment':
            await call.message.answer(
                text='пиши комент',
                parse_mode='HTML',
                reply_markup=reply.get_kb_back_to_menu()
            )

            # Устанавливаем состояние FSM в leave_comment
            await FSM.leave_comment.set()

        # Обработка кнопки '/main'
        if callback_data == '/main':
            # Возвращаемся в главное меню
            await call.message.answer(
                text=Texts.commands,
                parse_mode='HTML',
                reply_markup=reply.get_kb_menu()
            )

            # Устанавливаем состояние FSM в main_menu
            await FSM.main_menu.set()
    except Exception as e:
        print(f"An error occurred in def callback_inl_kb_after_swag: {str(e)}")


async def callback_decision_to_upload_photo(call: CallbackQuery, state: FSMContext):
    """
    Обработчик для реагирования на нажатие кнопок в меню решения о загрузке фото.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Данные полученные с inline-кнопок
        callback_data = call.data
        if callback_data == '/get_photo':
            # Запрашиваем загрузку фото и устанавливаем состояние FSM в get_photo
            await call.message.answer(
                text=Texts.set_the_photo,
                reply_markup=reply.get_kb_back_to_menu()
            )

            # Устанавливаем состояние FSM в get_photo
            await FSM.get_photo.set()

        elif callback_data == '/no_get_photo':
            # Сохраняем отсутствие фото ('0') в состояние и завершаем процесс создания
            async with state.proxy() as data:
                data['url'] = '0'

            # Отправляем сообщение об успешном создании с эмодзи и кнопками
            await call.message.answer(
                text=emojize(string=random_emoji_after_create()),
                reply_markup=ReplyKeyboardRemove()
            )
            await call.message.answer(
                text=Texts.done,
                parse_mode='HTML',
                reply_markup=inline.get_inl_kb_after_create()
            )

            # Устанавливаем состояние FSM в after_create
            await FSM.after_create.set()
    except Exception as e:
        print(f"An error occurred in def callback_decision_to_upload_photo: {str(e)}")


async def callback_inl_kb_after_create(call: CallbackQuery, state: FSMContext):
    """
    Обработчик для реагирования на нажатие кнопок после создания карточки.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Получаем данные из MemoryStorage
        data = await state.get_data()

        # Данные полученные с inline-кнопок
        callback_data = call.data

        # Обработка кнопки '/create'
        if callback_data == '/create':
            # Вставляем данные в базу данных и переходим к вводу нового слова
            insert.insert_into_main_library(
                username=call.from_user.username,
                word=data['word'],
                definition=data['desc'],
                url=data['url']
            )
            await call.message.answer(
                text=Texts.set_the_word,
                reply_markup=reply.get_kb_back_to_menu()
            )

            # Устанавливаем состояние FSM в get_word
            await FSM.get_word.set()

        # Обработка кнопки '/main'
        if callback_data == '/main':
            # Вставляем данные в базу данных и возвращаемся в главное меню
            insert.insert_into_main_library(
                username=call.from_user.username,
                word=data['word'],
                definition=data['desc'],
                url=data['url']
            )
            await call.message.answer(
                text=Texts.commands,
                parse_mode='HTML',
                reply_markup=reply.get_kb_menu()
            )

            # Устанавливаем состояние FSM в main_menu
            await FSM.main_menu.set()

        # Обработка кнопки '/shared'
        if callback_data == '/shared':
            # Вставляем данные в базу данных и переходим к FSM after_shared
            insert.insert_into_main_library(
                username=call.from_user.username,
                word=data['word'],
                definition=data['desc'],
                url=data['url'],
                shared='Yes'
            )
            await call.message.answer(
                text=Texts.after_add_to_shared.format(call.from_user.first_name),
                parse_mode='HTML',
                reply_markup=inline.get_inl_kb_after_shared()
            )

            # Устанавливаем состояние FSM в after_shared
            await FSM.after_shared.set()
    except Exception as e:
        print(f"An error occurred in def callback_inl_kb_after_create: {str(e)}")


async def callback_inl_kb_after_shared(call: CallbackQuery):
    """
    Обработчик для реагирования на нажатие кнопок после добавления карточки в shared.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
    """
    try:
        # Данные полученные с inline-кнопок
        callback_data = call.data

        # Обработка кнопки '/create'
        if callback_data == '/create':
            # Переходим к вводу нового слова
            await call.message.answer(
                text=Texts.set_the_word,
                reply_markup=reply.get_kb_back_to_menu()
            )

            # Устанавливаем состояние FSM в get_word
            await FSM.get_word.set()

        # Обработка кнопки '/main'
        if callback_data == '/main':
            # Возвращаемся в главное меню
            await call.message.answer(
                text=Texts.commands,
                parse_mode='HTML',
                reply_markup=reply.get_kb_menu()
            )

            # Устанавливаем состояние FSM в main_menu
            await FSM.main_menu.set()
    except Exception as e:
        print(f"An error occurred in def callback_inl_kb_after_shared: {str(e)}")


async def callback_inl_decision_what_train(call: CallbackQuery, state: FSMContext):
    """
    Обработчик для реагирования на нажатие кнопок в меню выбора типа тренировки (shared or personal).

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
        state (FSMContext): Объект для управления состоянием конечного автомата.
    """
    try:
        # Данные полученные с inline-кнопок
        callback_data = call.data

        # Обработка кнопки '/shared'
        if callback_data == '/shared':
            # Получаем все shared слова из базы данных
            all_items = get.select_shared_from_main_library()

            # Проверяем, есть ли слова для тренировки
            if all_items:
                await call.message.answer(
                    text=Texts.lets_go,
                    parse_mode='HTML'
                )
                await after_decision_what_train(
                    message=call.message,
                    all_items=all_items,
                    state=state
                )
            else:
                # Если нет shared слов, предлагаем создать
                await call.message.answer(
                    text=Texts.no_words_in_shared,
                    parse_mode='HTML',
                    reply_markup=inline.get_inl_kb_when_user_dont_have_any_words()
                )

                # Устанавливаем состояние FSM в no_words
                await FSM.no_words.set()

        # Обработка кнопки '/personal'
        if callback_data == '/personal':
            # Получаем все personal слова пользователя из базы данных
            all_items = get.select_not_shared_from_main_library(
                username=call.from_user.username
            )

            # Проверяем, есть ли слова для тренировки
            if all_items:
                await call.message.answer(
                    text=Texts.lets_go,
                    parse_mode='HTML'
                )
                await after_decision_what_train(
                    message=call.message,
                    all_items=all_items,
                    state=state
                )

            # Если нет personal слов, предлагаем создать
            else:
                await call.message.answer(
                    text=Texts.no_words_in_personal,
                    parse_mode='HTML',
                    reply_markup=inline.get_inl_kb_when_user_dont_have_any_words()
                )

                # Устанавливаем состояние FSM в no_words
                await FSM.no_words.set()
    except Exception as e:
        print(f"An error occurred in def callback_inl_decision_what_train: {str(e)}")


async def callback_inl_if_no_words(call: CallbackQuery):
    """
    Обработчик для реагирования на нажатие кнопок в меню, когда у пользователя нет слов для тренировки.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
    """
    try:
        # Данные полученные с inline-кнопок
        callback_data = call.data

        # Обработка кнопки '/create'
        if callback_data == '/create':
            # Переходим к вводу нового слова
            await call.message.answer(
                text=Texts.set_the_word,
                reply_markup=reply.get_kb_back_to_menu()
            )

            # Устанавливаем состояние FSM в get_word
            await FSM.get_word.set()

        # Обработка кнопки '/main'
        if callback_data == '/main':
            # Возвращаемся в главное меню
            await call.message.answer(
                text=Texts.commands,
                parse_mode='HTML',
                reply_markup=reply.get_kb_menu()
            )

            # Устанавливаем состояние FSM в main_menu
            await FSM.main_menu.set()
    except Exception as e:
        print(f"An error occurred in def callback_inl_if_no_words: {str(e)}")


async def callback_inl_kb_after_delete_word(call: CallbackQuery):
    """
    Обработчик для реагирования на нажатие кнопок после удаления слова.

    Args:
        call (CallbackQuery): Объект callback-запроса от пользователя.
    """
    try:
        # Данные полученные с inline-кнопок
        callback_data = call.data

        # Обработка кнопки '/delete'
        if callback_data == '/delete':
            # Запрашиваем слово для удаления и переходим к удалению
            await call.message.answer(
                text=Texts.delete,
                reply_markup=reply.get_kb_back_to_menu()
            )

            # Устанавливаем состояние FSM в delete_input
            await FSM.delete_input.set()

        # Обработка кнопки '/main'
        if callback_data == '/main':
            # Возвращаемся в главное меню
            await call.message.answer(
                text=Texts.commands,
                parse_mode='HTML',
                reply_markup=reply.get_kb_menu()
            )

            # Устанавливаем состояние FSM в main_menu
            await FSM.main_menu.set()
    except Exception as e:
        print(f"An error occurred in def callback_inl_kb_after_delete_word: {str(e)}")



def register_user_handlers(dp: Dispatcher) -> None:
    """
    Регистрация обработчиков сообщений пользователя.

    Args:
        dp (Dispatcher): Объект диспетчера для регистрации обработчиков.
    """
    try:
        dp.register_message_handler(callback=back_to_menu, commands=['back_to_menu'], state='*')
        dp.register_message_handler(callback=start, commands=['start'])
        dp.register_message_handler(callback=help_me_someone, commands=['help'])
        dp.register_message_handler(callback=menu, commands=['menu'], state=FSM.main_menu)
        dp.register_message_handler(callback=create_card, commands=['create'], state=FSM.main_menu)
        dp.register_message_handler(callback=get_photo, content_types=['photo'], state=FSM.get_photo)
        dp.register_message_handler(callback=get_desc, state=FSM.get_desc)
        dp.register_message_handler(callback=get_word, state=FSM.get_word)
        dp.register_message_handler(callback=start_train, commands=['train'], state=FSM.main_menu)
        dp.register_message_handler(callback=answer, commands=['answer'], state=FSM.answer)
        dp.register_message_handler(callback=next_word, commands=['next'], state=FSM.next_word)
        dp.register_message_handler(callback=count_words, commands=['count'], state=FSM.main_menu)
        dp.register_message_handler(callback=authors, commands=['authors'], state=FSM.main_menu)
        dp.register_message_handler(callback=delete_start, commands=['delete'], state=FSM.main_menu)
        dp.register_message_handler(callback=delete_input, state=FSM.delete_input)
        dp.register_message_handler(callback=swag, commands=['swag'], state=FSM.main_menu)
        dp.register_message_handler(callback=leave_comment_in_db, state=FSM.leave_comment)
    except Exception as e:
        print(f"An error occurred in def register_user_handlers: {str(e)}")


def register_user_callback_query_handlers(dp: Dispatcher) -> None:
    """
    Регистрация обработчиков callback-запросов пользователя.

    Args:
        dp (Dispatcher): Объект диспетчера для регистрации обработчиков.
    """
    try:
        dp.register_callback_query_handler(
            callback_inl_kb_after_create, lambda call: True, state=FSM.after_create
        )
        dp.register_callback_query_handler(
            callback_inl_kb_after_shared, lambda call: True, state=FSM.after_shared
        )
        dp.register_callback_query_handler(
            callback_decision_to_upload_photo, lambda call: True, state=FSM.decision_to_upload_photo
        )
        dp.register_callback_query_handler(
            callback_inl_decision_what_train, lambda call: True, state=FSM.decision_what_train
        )
        dp.register_callback_query_handler(
            callback_inl_if_no_words, lambda call: True, state=FSM.no_words
        )
        dp.register_callback_query_handler(
            callback_inl_kb_after_delete_word, lambda call: True, state=FSM.after_delete
        )
        dp.register_callback_query_handler(
            callback_inl_kb_after_swag, lambda call: True, state=FSM.after_swag
        )
    except Exception as e:
        print(f"An error occurred in def register_user_callback_query_handlers: {str(e)}")
