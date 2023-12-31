from emoji import emojize

class Texts:
    # user_handler_texts:
    commands = (
        '<u><b>C O M M A N D</b></u>' + emojize('🐢') + '<u><b>L I S T</b></u>:\n' 
        '🐸 Создать карточку: /create\n'
        '🧩 Начать тренить брейн: /train\n'
        '🔋 Сколько слов за пазухой: /count\n'
        '🌵 Кинуть слово в мусорку: /delete\n'
        '🌳 Засталкерить автора: /authors\n'
        '🌳 Оставить комментарий: /swag'
    )
    start = (
        '🎉 <b>Добро пожаловать, друзья!</b> 🎉\n\n'
        'Данное творение предназначено для создания карточек, которые помогут вам изучать новые слова, '
        'всякие нудные термины, определения и т.п. Ну и, конечно, <i>для рофлов))</i>\n\n'
        
        '<b><u>При создании карточки есть три этапа</u>:</b>\n\n'
        
        '🧿 <i><b>Слово</b></i>: Придумай слово для изучения (его ты будешь видеть в задаваемом вопросе)\n\n'
        '<u>Например</u>: что такое "рофл", Санчоус?\n\n'
        
        '🧿 <i><b>Определение</b></i>: Дай ему определение. \n\n'
        '<u>Например</u>: Рофл - это когда все рофлят с твоего рофла, но это может быть и кринж, если рофлишь с рофла только ты 🤔\n\n'
        
        '🧿 <i><b>Картинка</b></i>: К слову можно добавить картинку, чтобы запоминать новые слова прям супер жестко и быстро.\n\n'
        
        'Это по желанию, можешь не добавлять, если не хочешь.\n\n'
        
        '🌱 <b>Вам предстоит сложный выбор:</b> делиться или да 🌱\n\n'
        '<i><b>Personal:</b></i> Тут ваш личный space ship place 🏴‍☠️, никто не увидит слова, что вы создаете, так что сюда можно '
        'заливать все, что хотите! Даже английский 🐸\n\n'
        
        '<i><b>Shared:</b></i> Здесь другие пользователи могут покекать над вашими преколами или поучиться уму разуму с вашего'
        ' контента 🌚\n\n'
        
        '<b>W A R N I N G!</b>\n'
        'Перед тем, как поделиться карточкой в общей папке, задумайтесь: может ли она кого-то обидеть? задеть? навредить? оскорбить? '
        'Ну, вы поняли! Будьте, пожалуйста, толерантны и думайте перед тем, как отправить свои шутки))\n\n'

        
        '<b>P.S.</b><u>Если хочешь</u>, ты можешь оставить свое мнение / пожелание / предложение в комментах!)\n\n\n'
        
        
        '💚 В общем, приятного пользования! Надеюсь, вам понравится 💚\n'
        '<b>Нажимай кнопку /menu</b>'
    )
    set_the_word = '🌱 Введи слово'
    set_the_decs = '🌱 Введи определение слова'
    ask_to_set_the_photo = '🌱 Хочешь добавить к карточке фотографию?'
    set_the_photo = '🌱 Оки! Пришли, пожалуйста, фотографию'
    done = '<b>D O N E</b> 🐢'
    after_add_to_shared = '🌱 Йоууу! Спасибо, что поделил<b><i><s>ся</s></i></b>ась, <i><b>{}!</b></i>'
    choose_what_train = '🌱 Куда пойдем?'
    answer = '🌱 <b>Ответ:</b> {}'
    question = '🌱 Что такое <b>{}</b>?'
    statistics = (
        '🌳 <b><u>S T A T I S T I C S</u></b> 🌳\n'
        'Всего слов: <b><i>{}</i></b>\n'
        'Personal: <b><i>{}</i></b>\n'
        'Shared: <b><i>{}</i></b>\n'
    )
    authors = '🌳 <b><u>A U T H O R 🌱 W O R D S</u></b> 🌳\n'
    delete = '🌱 Какое слово ты хочешь удалить?'
    word_not_found = '🌵 <i><b>Либо</b></i> ты опечатался, <i><b>либо</b></i> такого слова нет 🌵'
    lets_go = "<b>L E T' S 🌱 G O!</b>"
    no_words_in_shared = '🌵 В shared пока ничего нет 🐢, будь первым <i><b>мазафака!</b></i> 🌵'
    no_words_in_personal = '🌵 лол прикол.. <i><b>сначала создай слова))</b></i> 🌵'
    swag = "🌳 <b><u>S K I R M I S H E S</u></b> 🌳"

    # other_handler_texts:
    no_comments = 'Тут пока что пусто 🌚'
    echo_callback = '🌵 Выбери ответ из кнопочек <i><b>выше))</b></i> 🌵'
    echo_main_menu = '🌵 Выбери пункт из меню! 🌵'
    echo_help = '🌵 Введи /help чтобы увидеть <i><b>command list</b></i> 🌵'
    echo_not_photo = '🌵 Это не фото <i><b>мазафака</b></i> 🌵'
    echo_got_file = '🌵 Дядь, это не фото, <i><b>это файл</b></i> 🌵'
    echo_answer = (
        '🌵 <i><b>Или</b></i> ты вводишь что-то кроме /back_to_menu и /answer, \n'
        '<i><b>Или</b></i> ты нажимаешь на кнопки <i>слишком быстро))</i> 🌵'
    )
    echo_next = (
        '🌵 <i><b>Или</b></i> ты вводишь что-то кроме /back_to_menu и /next, \n'
        '<i><b>Или</b></i> ты нажимаешь на кнопки <i>слишком быстро))</i> 🌵'
    )

    # buttons
    go_to_the_menu = 'Упорхнуть в меню 🐝'
    comment = 'Оставить комментарий ✏️'
    another_one = 'Ещё по одной 🍺'
    create_when_no_words = 'Создать 🌚'
    add_to_shared = 'Добавить в shared 🐥'