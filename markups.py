import telebot
import knight as k
from telebot import types


def get_persons_markup():
    persons_markup = types.InlineKeyboardMarkup()
    for person in k.get_persons():
        persons_markup.add(types.InlineKeyboardButton(person, callback_data=person))
    persons_markup.add(types.InlineKeyboardButton(text='Члени ордену', callback_data='Члени ордену'))
    persons_markup.add(types.InlineKeyboardButton(text='На головну', callback_data='На головну'))
    persons_markup.add(types.InlineKeyboardButton(text='/stop', callback_data='/stop'))
    return persons_markup


def get_titles_markup():
    titles_markup = telebot.types.ReplyKeyboardMarkup(True)
    for person in k.get_titles():
        titles_markup.row(person)
    titles_markup.row('Члени ордену')
    titles_markup.row('На головну')
    titles_markup.row('/stop')
    return titles_markup


def get_members_order_markup():
    members_order_markup = types.InlineKeyboardMarkup()
    members_order_text = (
        'Список всіх членів ордену', 'Надати довідку про члена ордену', 'Додати Послушника', 'Видалити еретика',
        'На головну', '/stop')
    for text in members_order_text:
        members_order_markup.add(types.InlineKeyboardButton(text, callback_data=text))
    return members_order_markup


def get_person_titles_markup(name):
    person_titles_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    for title in k.get_person_titles(name):
        person_titles_markup.row(title)
    person_titles_markup.row('Члени ордену')
    person_titles_markup.row('На головну')
    person_titles_markup.row('/stop')
    return person_titles_markup


def get_person_long_drawer_markup(name):
    person_long_drawer_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    for i in k.get_person_long_drawer_topic(name):
        person_long_drawer_markup.row(i)
    person_long_drawer_markup.row('Члени ордену')
    person_long_drawer_markup.row('На головну')
    person_long_drawer_markup.row('/stop')
    return person_long_drawer_markup


def get_PTLDM(name, topic):
    PTLDM = telebot.types.ReplyKeyboardMarkup(True, True)
    for i in k.get_person_long_drawer(name, topic):
        PTLDM.row(str(i.message_content.decode('UTF-8')))
    PTLDM.row('Члени ордену')
    PTLDM.row('На головну')
    PTLDM.row('/stop')
    return PTLDM


main_text = ('Члени ордену', 'Титули', 'Довгий ящик', 'Постріл', '/stop')
main_markup = types.InlineKeyboardMarkup()
for text in main_text:
    main_markup.add(types.InlineKeyboardButton(text, callback_data=text))

titles_text = ('Надати титул персоні', 'Додати новий титул', 'Вилучити титул в недостойного',
               'Змінити званя члена ордену', 'Показати всі титули', 'Надати довідку про члена ордену',
               'Видалити титул зі списку', 'На головну', '/stop')
titles_markup = types.InlineKeyboardMarkup()
for text in titles_text:
    titles_markup.add(types.InlineKeyboardButton(text, callback_data=text))

standard_text = ('На головну', 'Члени ордену', '/stop')
standard_markup = types.InlineKeyboardMarkup()
for text in standard_text:
    standard_markup.add(types.InlineKeyboardButton(text, callback_data=text))

long_drawer_text = (
    'Наповнити довгий ящик', 'Показати засекречений матеріал', 'Видалити давнішню єресть', 'Видалити давнішню єресть',
    'На головну', 'Члени ордену', '/stop')
long_drawer_markup = types.InlineKeyboardMarkup()
for text in long_drawer_text:
    long_drawer_markup.add(types.InlineKeyboardButton(text, callback_data=text))
