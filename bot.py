# -*- coding: utf-8 -*-

"""
version 1.0 : основа бота, створення юзерів, титулів, надання титулів персоні, і тд.

version 1.1 : перша реалізація довгого ящика

version 1.2 : покращення довгого ящика, та додання методу для вибору випадкового юзера

version 2.0 : перехід на інлайн клавіші, бд Postgres та маленьки фікси

version 2.1 : допиленя інлайн клавішів, видалення довгого ящика за не надобністю, маленькі фікси

version 2.2 : Додання методів для створення, видалення викликів юзерів. та інші фікси

"""
import os

import knight as k
import youtube
import telebot
import constant
import markups
import requests
import json
import traceback
import random
import math
import time
import collections
import string

bot = telebot.TeleBot(constant.token)
user_dict = {}
home = os.getcwd()


class User:
    def __init__(self, name):
        self.name = name
        self.message = collections.deque(range(5), maxlen=5)


def add_call_history(function):
    def call_history(call):
        try:
            chat_id = call.message.chat.id
            text = call.data
            name = call.message.from_user.username
            add_user_message(chat_id, text, name)
            return function(call)
        except AttributeError:
            return function(call)

    return call_history


def add_message_history(function):
    def message_history(message):
        try:
            chat_id = message.chat.id
            text = message.text
            name = message.from_user.username
            add_user_message(chat_id, text, name)
            return function(message)
        except AttributeError:
            return function(message)

    return message_history


def add_user_message(chat_id, text, name):
    if chat_id in user_dict:
        user = user_dict[chat_id]
        user.message.append(text)
    else:
        user = User(name)
        user.message.append(text)
        user_dict[chat_id] = user
    # print(user.message)


def if_not_standard(message):
    text = message.text.replace(' ', '')
    if '!' in text:
        name = text.translate(str.maketrans('', '', string.punctuation)).lower()
        person = k.get_person_for_call_name(name)
        if person:
            message_text = k.get_person_user_name(person) + ' ' + get_person_status(person) + ' Викликаємо тебе!'
            bot.send_message(message.chat.id, message_text)
        if name == "all":
            message_text = "@West_Lion @Sasha_Korenivsky @noctua_rb @AndriySikora @tewtydry @DmitrDX @OscarD @globalus @qu4cken @V_Van_Gogh @575505064 Всі Всі Всі, тут шото хочуть!"
            bot.send_message(message.chat.id, message_text)
        return False
    return message


def butter(chat_id):
    img = open("{}butter.jpeg".format(home), "rb")
    bot.send_message(chat_id, "Для чого я створений?")
    time.sleep(2)
    bot.send_message(chat_id, "щоб носити масло")
    bot.send_photo(chat_id, img)
    img.close()


@bot.message_handler(commands=["start"])
def handler_start(message):
    bot.send_message(message.chat.id, text="В якому ж ти відчаї раз звернувся до мене?",
                     reply_markup=markups.main_markup)


@bot.callback_query_handler(func=lambda call: call.data == "/stop")
def handler_stop(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="See you in hell!")


@bot.message_handler(commands=["stop"])
def handler_stop(message):
    bot.send_message(message.chat.id, "See you in hell!")


@bot.message_handler(content_types=["text"])
@add_message_history
def handler_text(message):
    # print(message)
    text = message.text
    audio = open("{}tamam_tamam.mp3".format(home), "rb")
    standard_messages = {
        "easy easy": lambda: bot.send_audio(message.chat.id, audio),
        "создатєль": lambda: butter(message.chat.id),
        "постріл": lambda: bot.send_message(message.chat.id, get_random_person()),
        "підр": lambda: bot.send_message(message.chat.id, get_random_person_without_name(message)),
        "курс": lambda: bot.send_message(message.chat.id, get_exchange_rates()),
        "music": lambda: bot.register_next_step_handler(
            bot.reply_to(message, "Введіть назву"),
            get_name_music)
    }
    if text.lower() in ['підр', 'підар', 'пiдaр', 'пiдap', 'підaр', 'підаp', 'мужеложець', '3.14дар']:
        text = 'підр'

    if text.lower() in standard_messages:
        standard_messages[text.lower()]()
    elif text in k.get_persons():
        send_text = get_person_status(text)
        bot.send_message(message.chat.id, send_text)
    elif "random" in text.lower() or "рандом" in text.lower() or "roll" in text.lower():
        send_random_number(message)
    else:
        if not if_not_standard(message):
            pass
    audio.close()


def get_random_person():
    return k.get_persons()[math.floor(random.random() * len(k.get_persons()) - 1)]


def send_random_number(message):
    try:
        second_number = int(message.text.lower().split()[-1])
        if second_number > 0:
            if "to" in message.text.lower():
                firs_number = int(message.text.lower().split()[-3])
                if firs_number > 0:
                    bot.send_message(message.chat.id, str(random.randint(firs_number, second_number)))
                else:
                    bot.send_message(message.chat.id, "рандом працює тільки з цілими додатніми числами")
            else:
                bot.send_message(message.chat.id, str(random.randint(1, second_number)))
        else:
            bot.send_message(message.chat.id, "рандом працює тільки з цілими додатніми числами")
    except ValueError:
        pass


def get_random_person_without_name(message):
    name = get_random_person()
    if message.from_user.id == k.get_person_user_id(name) or k.get_person_user_id(name) == 575505064:
        return get_random_person_without_name(message)
    return name


def get_person_status(name):
    return k.get_person_rank(name) + ' ' + ', '.join(
        k.get_person_titles(name)) + ' ' + name + '.'


def get_exchange_rates():
    r = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
    result = ""
    for i in json.loads(r.text)[:3]:
        result += "{} {} - {}\n".format(i['ccy'], i['buy'], i['sale'])
    return result


def show_persons_call_name():
    persons_call_name = k.get_persons_call_name()
    result = "Варіанти виклику:\n"
    for person in persons_call_name:
        result += "{} : {}.\n".format(person, ', '.join(persons_call_name[person]))
    return result


@add_message_history
def get_name_music(message):
    global y
    y = youtube.YoutubeParser()
    y.get_music_links(message.text)
    msg = bot.reply_to(message, 'Обирай пісню', reply_markup=y.get_music_markups())
    bot.register_next_step_handler(msg, get_href_music)


@bot.callback_query_handler(func=lambda call: "YBM" in call.data)
@add_call_history
def get_href_music(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=y.get_music_href(call.data[3:]))


def del_title_in_list(call):
    try:
        k.del_title(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Титул вилучено зі списку", reply_markup=markups.titles_markup)
    except Exception:
        print(traceback.format_exc())


@add_message_history
def new_title(message):
    try:
        k.set_title(message.text)
        bot.reply_to(message, "Титул успішно додано!", reply_markup=markups.titles_markup)
    except Exception as e:
        print(traceback.format_exc())
        bot.reply_to(message, "oooops")


def set_title(call):
    try:
        user = user_dict[call.message.chat.id]
        if user.message[-2] in k.get_persons():
            if k.set_person_title(user.message[-2], call.data):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Титул успішно надано!", reply_markup=markups.titles_markup)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Титул вже надано",
                                      reply_markup=markups.titles_markup)
    except Exception:
        print(traceback.format_exc())
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="oooops")


def up_rank(call):
    try:
        user = user_dict[call.message.chat.id]
        k.replace_rank(user.message[-2], call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Звання успішно змінено!", reply_markup=markups.titles_markup)

    except Exception:
        print(traceback.format_exc())
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="oooops")


@add_message_history
def add_person(message):
    try:
        k.set_person(message.text)
        bot.reply_to(message, text="Ооо, свіже м'ясо", reply_markup=markups.get_members_order_markup())
    except Exception as e:
        bot.reply_to(message, text="oooops")
        print(traceback.format_exc())


@bot.callback_query_handler(func=lambda call: call.data in k.get_persons() and user_dict[call.message.chat.id].message[
    -1] == "Видалити еретика")
@add_call_history
def del_person(call):
    try:
        k.del_person(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Інквізиція успішно виконала свою справу",
                              reply_markup=markups.get_members_order_markup())
    except Exception as e:
        print(traceback.format_exc())


def del_person_title(call):
    try:
        user = user_dict[call.message.chat.id]
        k.del_person_title(user.message[-2], call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Звання вилучено в недостойного!", reply_markup=markups.titles_markup)

    except Exception:
        print(traceback.format_exc())
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="oooops")


@add_message_history
def add_person_call_name(message):
    user = user_dict[message.chat.id]
    person = user.message[-2]
    k.set_person_call_name(person, message.text)
    bot.reply_to(message, "Додано, спробуйте викликати його ввівши {}!".format(message.text))


def del_person_call_name(call):
    try:
        k.del_person_call_name(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Виклик вилучено!", reply_markup=markups.standard_markup)

    except Exception:
        print(traceback.format_exc())
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="oooops")


# class SecretBasket:
#     def __init__(self):
#         self.secret_basket = []
#
#     def add_person_to_secret_basket(self, person):
#         self.secret_basket.append(person.lower())
#
#     def get_secret_basket_len(self) -> str:
#         return str(len(self.secret_basket))
#
#     def get_random_person_without_yourself(self, person) -> str:
#         if self.secret_basket:
#             if len(self.secret_basket) == 1 and person in self.secret_basket:
#                 return "в кошику знаходиться тільки ваше ім'я, але я думаю що краще 'гратися' сам з собою по іншому)"
#             else:
#                 name = self.secret_basket[math.floor(random.random() * len(self.secret_basket) - 1)]
#                 if person == name:
#                     return self.get_random_person_without_yourself(person)
#                 else:
#                     self.secret_basket.remove(name)
#                     return f'Жертва для дарунку - {name}'
#         else:
#             return "Гей, схоже шапка дірява. Бо я не бачу тут жодного імені!"
#
#     def clear_secret_basket(self):
#         self.secret_basket.clear()
#
#
# SECRET_BASKET = SecretBasket()


# @add_call_history
# def add_person_to_secret_basket(message):
#     SECRET_BASKET.add_person_to_secret_basket(person=message.text.lower())
#     bot.reply_to(message, text="Вітаю, ви віддалися на волю 'рандому')", reply_markup=markups.secret_basket_markup)
#
#
# @add_message_history
# def get_person_from_secret_basket(message):
#     bot.reply_to(message, text=SECRET_BASKET.get_random_person_without_yourself(message.text.lower()),
#                  reply_markup=markups.secret_basket_markup)
#
#
# def get_size_secret_basket() -> str:
#     return f'Кількість душ що підписали контракт про нерозголошення : {SECRET_BASKET.get_secret_basket_len()}'
#
#
# def clear_secret_basket() -> str:
#     SECRET_BASKET.clear_secret_basket()
#     return f'Щож всі данні знищено ніхто нікого не знає, ніхто нікого не бачив...'


@bot.callback_query_handler(func=lambda call: True)
@add_call_history
def standard_callback_data(call):
    # print(call)
    standard_CD = {
        "члени ордену": lambda: bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                      text="Обирай!", reply_markup=markups.get_members_order_markup()),
        "титули": lambda: bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text="Обирай!", reply_markup=markups.titles_markup),
        "на головну": lambda: bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                    text="Головну сторінку активовано",
                                                    reply_markup=markups.main_markup),
        "список всіх членів ордену": lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                                   message_id=call.message.message_id,
                                                                   text=",\n".join(sorted(k.get_persons())),
                                                                   reply_markup=markups.standard_markup),
        "надати довідку про члена ордену": lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                                         message_id=call.message.message_id,
                                                                         text="Обирай!",
                                                                         reply_markup=markups.get_persons_markup()),
        "показати всі титули": lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                             message_id=call.message.message_id,
                                                             text=",\n".join(sorted(k.get_titles())),
                                                             reply_markup=markups.standard_markup),
        "додати послушника": lambda: bot.register_next_step_handler(
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Введіть ім'я цього відчайдухи"), add_person),
        "Видалити еретика".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                                  message_id=call.message.message_id,
                                                                  text="Оберіть ім'я цього еретика",
                                                                  reply_markup=markups.get_persons_markup()),
        "Надати титул персоні".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                                      message_id=call.message.message_id,
                                                                      text="Оберіть ім'я цього посвяченого",
                                                                      reply_markup=markups.get_persons_markup()),
        "Вилучити титул в недостойного".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                                               message_id=call.message.message_id,
                                                                               text="Оберіть ім'я цього посвяченого",
                                                                               reply_markup=markups.get_persons_markup()),
        "Змінити званя члена ордену".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                                            message_id=call.message.message_id,
                                                                            text="Оберіть ім'я цього посвяченого",
                                                                            reply_markup=markups.get_persons_markup()),
        "Видалити титул зі списку".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                                          message_id=call.message.message_id,
                                                                          text="Виберіть титул який бажаєте видалити",
                                                                          reply_markup=markups.get_titles_markup()),
        "Додати новий титул".lower(): lambda: bot.register_next_step_handler(
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Введіть новий титул"), new_title),
        "Додати виклик члена ордену".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                                            message_id=call.message.message_id,
                                                                            text="Оберіть ім'я цього посвяченого",
                                                                            reply_markup=markups.get_persons_markup()),
        "Показати варіанти призиву".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
                                                                           message_id=call.message.message_id,
                                                                           text=show_persons_call_name(),
                                                                           reply_markup=markups.standard_markup),
        "Видалити варіант призиву".lower(): lambda: bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Оберіть ім'я цього ноунейма",
            reply_markup=markups.get_persons_markup()),
        # "Таємний санта".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
        #                                                        message_id=call.message.message_id,
        #                                                        text="Йо-хо-хо, ну ти й відчайдух, сам вирішив підписатися на цю гру",
        #                                                        reply_markup=markups.secret_basket_markup),
        # "Додати себе у капелюх".lower(): lambda: bot.register_next_step_handler(
        #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
        #                           text="Введіть своє ім'я"), add_person_to_secret_basket),
        # "Дістати жертву".lower(): lambda: bot.register_next_step_handler(
        #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
        #                           text="Але спочатку ведіть своє ім'я, яке вказували, щоб випадково не самовипилитися"),
        #     get_person_from_secret_basket),
        # "Скіко вже душ зібрано".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
        #                                                                message_id=call.message.message_id,
        #                                                                text=get_size_secret_basket(),
        #                                                                reply_markup=markups.secret_basket_markup),
        # "Очистити ту драну шапку".lower(): lambda: bot.edit_message_text(chat_id=call.message.chat.id,
        #                                                                  message_id=call.message.message_id,
        #                                                                  text=clear_secret_basket(),
        #                                                                  reply_markup=markups.secret_basket_markup),

    }

    if call.data.lower() in standard_CD:
        standard_CD[call.data.lower()]()
    elif user_dict[call.message.chat.id].message[-3] == "Видалити варіант призиву":
        del_person_call_name(call)
    elif call.data in k.get_persons() and user_dict[call.message.chat.id].message[
        -2] == "Вилучити титул в недостойного":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Оберіть титул",
                              reply_markup=markups.get_person_titles_markup(call.data))
    elif call.data in k.get_titles() and user_dict[call.message.chat.id].message[-3] == "Вилучити титул в недостойного":
        del_person_title(call)
    elif call.data in k.get_persons() and user_dict[call.message.chat.id].message[-2] == "Видалити варіант призиву":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Оберіть варіант виклику",
                              reply_markup=markups.get_call_name_for_person(call.data))
    elif call.data in k.get_persons() and user_dict[call.message.chat.id].message[-2] == "Додати виклик члена ордену":
        bot.register_next_step_handler(
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="введіть поганяло для виклику"), add_person_call_name)
    elif call.data in k.get_persons() and user_dict[call.message.chat.id].message[-2] == "Змінити званя члена ордену":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Оберіть звання",
                              reply_markup=markups.get_titles_markup())
    elif call.data in k.get_titles() and user_dict[call.message.chat.id].message[-3] == "Змінити званя члена ордену":
        up_rank(call)
    elif call.data in k.get_persons() and user_dict[call.message.chat.id].message[-2] == "Надати титул персоні":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Оберіть титул",
                              reply_markup=markups.get_titles_markup())
    elif call.data in k.get_titles() and user_dict[call.message.chat.id].message[-3] == "Надати титул персоні":
        set_title(call)
    elif call.data in k.get_titles() and user_dict[call.message.chat.id].message[-2] == "Видалити титул зі списку":
        del_title_in_list(call)
    elif call.data in k.get_persons():
        text = get_person_status(call.data)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=markups.get_persons_markup())
    else:
        pass


def main():
    try:
        print("БОТ V_2.1 activation")
        bot.polling(none_stop=True, interval=0)
        print("БОТ V_2.1 зупинився")
    except Exception:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
