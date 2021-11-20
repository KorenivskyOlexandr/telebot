import knight as k
from telebot import types


def add_standard_markup(inline_markup):
    for name in ['Члени ордену', 'Титули', 'На головну', '/stop']:
        inline_markup.add(types.InlineKeyboardButton(text=name, callback_data=name))
    return inline_markup


def get_persons_markup():
    persons_markup = types.InlineKeyboardMarkup()
    for person in k.get_persons():
        persons_markup.add(types.InlineKeyboardButton(person, callback_data=person))
    persons_markup = add_standard_markup(persons_markup)
    return persons_markup


def get_titles_markup():
    titles_markup = types.InlineKeyboardMarkup()
    for title in k.get_titles():
        titles_markup.add(types.InlineKeyboardButton(title, callback_data=title))
    titles_markup = add_standard_markup(titles_markup)
    return titles_markup


def get_members_order_markup():
    members_order_markup = types.InlineKeyboardMarkup()
    members_order_text = (
        'Список всіх членів ордену', 'Надати довідку про члена ордену', 'Додати Послушника', 'Видалити еретика',
        'Додати виклик члена ордену', 'Показати варіанти призиву', "Видалити варіант призиву",
        'На головну', '/stop')
    for text in members_order_text:
        members_order_markup.add(types.InlineKeyboardButton(text, callback_data=text))
    return members_order_markup


def get_person_titles_markup(name):
    person_titles_markup = types.InlineKeyboardMarkup()
    for title in k.get_person_titles(name):
        person_titles_markup.add(types.InlineKeyboardButton(title, callback_data=title))
    person_titles_markup = add_standard_markup(person_titles_markup)
    return person_titles_markup


def get_call_name_for_person(person):
    call_name_for_person_markup = types.InlineKeyboardMarkup()
    for call_name in k.get_call_name_for_person(person):
        call_name_for_person_markup.add(types.InlineKeyboardButton(call_name, callback_data=call_name))
    call_name_for_person_markup = add_standard_markup(call_name_for_person_markup)
    return call_name_for_person_markup


main_text = ('Члени ордену', 'Титули', 'Таємний санта', '/stop')
main_markup = types.InlineKeyboardMarkup()
for text in main_text:
    main_markup.add(types.InlineKeyboardButton(text, callback_data=text))

titles_text = ('Надати титул персоні', 'Додати новий титул', 'Вилучити титул в недостойного',
               'Змінити званя члена ордену', 'Показати всі титули', 'Надати довідку про члена ордену',
               'Видалити титул зі списку', 'На головну', '/stop')
titles_markup = types.InlineKeyboardMarkup()
for text in titles_text:
    titles_markup.add(types.InlineKeyboardButton(text, callback_data=text))

standard_text = ('На головну', 'Титули', 'Члени ордену', '/stop')
standard_markup = types.InlineKeyboardMarkup()
for text in standard_text:
    standard_markup.add(types.InlineKeyboardButton(text, callback_data=text))

secret_basket_text = (
    'На головну', 'Додати себе у капелюх', 'Дістати жертву',
    'Скіко вже душ зібрано', 'Очистити ту драну шапку', '/stop')
secret_basket_markup = types.InlineKeyboardMarkup()
for text in secret_basket_text:
    secret_basket_markup.add(types.InlineKeyboardButton(text, callback_data=text))


