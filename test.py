import telebot
from telebot import types

token = "your token"
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
    second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
    keyboardmain.add(first_button, second_button)
    bot.send_message(message.chat.id, "testing kb", reply_markup=keyboardmain)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "mainmenu":
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        first_button = types.InlineKeyboardButton(text="1button", callback_data="first")
        second_button = types.InlineKeyboardButton(text="2button", callback_data="second")
        keyboardmain.add(first_button, second_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="menu",
                              reply_markup=keyboardmain)

    if call.data == "first":
        keyboard = types.InlineKeyboardMarkup()
        rele1 = types.InlineKeyboardButton(text="1t", callback_data="1")
        rele2 = types.InlineKeyboardButton(text="2t", callback_data="2")
        rele3 = types.InlineKeyboardButton(text="3t", callback_data="3")
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard.add(rele1, rele2, rele3, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="replaced text",
                              reply_markup=keyboard)

    elif call.data == "second":
        keyboard = types.InlineKeyboardMarkup()
        rele1 = types.InlineKeyboardButton(text="another layer", callback_data="gg")
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard.add(rele1, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="replaced text",
                              reply_markup=keyboard)

    elif call.data == "1" or call.data == "2" or call.data == "3":
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="alert")
        keyboard3 = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="lastlayer", callback_data="ll")
        keyboard3.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="last layer",
                              reply_markup=keyboard3)

if __name__ == "__main__":
    bot.polling(none_stop=True)

test = {'game_short_name': None,
        'chat_instance': '2700578855274192888',
        'id': '1473063851808272767',
        'from_user': {'id': 342974404,
                      'is_bot': False,
                      'first_name': 'Саша',
                      'username': 'Sasha_Korenivsky', 'last_name': 'Коренівський', 'language_code': 'uk'},
        'message': {'content_type': 'text', 'message_id': 5013,
                    'from_user': '<telebot.types.User object at 0x7f394dfc2278>', 'date': 1582037161,
                    'chat': '<telebot.types.Chat object at 0x7f394dfc2b00>', 'forward_from_chat': None,
                    'forward_from_message_id': None, 'forward_from': None, 'forward_date': None,
                    'reply_to_message': '<telebot.types.Message object at 0x7f394dfcbc50>', 'edit_date': None,
                    'media_group_id': None, 'author_signature': None, 'text': 'Обирай пісню', 'entities': None,
                    'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None,
                    'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None,
                    'location': None, 'venue': None, 'animation': None, 'new_chat_member': None,
                    'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None,
                    'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None,
                    'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None,
                    'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None,
                    'json': {'message_id': 5013, 'from': {'id': 794018685, 'is_bot': True, 'first_name': 'Val_Marafon',
                                                          'username': 'Val_Marafon_bot'},
                             'chat': {'id': 342974404, 'first_name': 'Саша', 'last_name': 'Коренівський',
                                      'username': 'Sasha_Korenivsky', 'type': 'private'},
                             'date': 1582037161,
                             'reply_to_message': {'message_id': 5012,
                                                  'from': {'id': 342974404, 'is_bot': False, 'first_name': 'Саша',
                                                           'last_name': 'Коренівський', 'username': 'Sasha_Korenivsky',
                                                           'language_code': 'uk'},
                                                  'chat': {'id': 342974404, 'first_name': 'Саша',
                                                           'last_name': 'Коренівський', 'username': 'Sasha_Korenivsky',
                                                           'type': 'private'}, 'date': 1582037160, 'text': 'ACDC'},
                             'text': 'Обирай пісню',
                             'reply_markup': {'inline_keyboard': [
                                 [{'text': '0', 'callback_data': 'AC/DC - Thunderstruck (Official Video)'}],
                                 [{'text': '1', 'callback_data': 'AC/DC - Highway to Hell (from Live at River Plate)'}],
                                 [{'text': '2', 'callback_data': 'AC/DC - Back In Black (Official Video)'}],
                                 [{'text': '3', 'callback_data': 'ACDC Live @ Munich STIFF UPPER LIP 2001 Concert'}],
                                 [{'text': '4', 'callback_data': 'AC/DC - Highway to Hell (Official Video)'}]]}}},
        'data': 'AC/DC - Highway to Hell (from Live at River Plate)', 'inline_message_id': None}
tt = {'message_id': 5043,
      'from': {'id': 794018685, 'is_bot': True, 'first_name': 'Val_Marafon', 'username': 'Val_Marafon_bot'},
      'chat': {'id': 342974404, 'first_name': 'Саша', 'last_name': 'Коренівський', 'username': 'Sasha_Korenivsky',
               'type': 'private'}, 'date': 1582100544, 'reply_to_message': {'message_id': 5042,
                                                                            'from': {'id': 342974404, 'is_bot': False,
                                                                                     'first_name': 'Саша',
                                                                                     'last_name': 'Коренівський',
                                                                                     'username': 'Sasha_Korenivsky',
                                                                                     'language_code': 'uk'},
                                                                            'chat': {'id': 342974404,
                                                                                     'first_name': 'Саша',
                                                                                     'last_name': 'Коренівський',
                                                                                     'username': 'Sasha_Korenivsky',
                                                                                     'type': 'private'},
                                                                            'date': 1582100544, 'text': 'tamam tamam'},
      'text': 'Обирай пісню',
      'reply_markup': {
        'inline_keyboard': [[{'text': 'Summer Cem - "TMM TMM" (official Video) prod. by Miksu', 'callback_data': '0'}],
                            [{'text': 'Summer Cem  TAMAM TAMAM  [ official Video ] prod. by Miksu',
                              'callback_data': '1'}],
                            [{'text': 'Deniz Cem - Tamam Tamam (Produced by Shabda)', 'callback_data': '2'}],
                            [{'text': 'Summer Cem - TMM TMM (Ilkay Sencan Remix)', 'callback_data': '3'}]]}}
