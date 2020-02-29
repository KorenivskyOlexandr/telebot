# -*- coding: utf-8 -*-

import traceback
import collections
import psycopg2

myDB = psycopg2.connect(
  database="bot_db",
  user="telebot",
  password="adminBot",
  host="127.0.0.1",
  port="5432"
)
my_cursor = myDB.cursor()


def set_person(name):
    my_cursor.execute("INSERT INTO persons (person, rank_id) VALUES ('{}', 13)".format(name))
    myDB.commit()


def set_title(new_title):
    my_cursor.execute("INSERT INTO titles (title) VALUES ('{}')".format(new_title))
    myDB.commit()


def set_person_title(person, title):
    my_cursor.execute("""SELECT k.* FROM knights k, persons p, titles t
                            WHERE k.person_id = p.id 
                            and k.title_id = t.id
                            and p.person = '{}'
                            and t.title = '{}'
                            """.format(person, title))

    if len(my_cursor.fetchall()) > 0:
        return False

    my_cursor.execute("""INSERT INTO knights (person_id, title_id) VALUES (
                    (SELECT id FROM persons WHERE person='{}'),
                    (SELECT id FROM titles WHERE title='{}')
                    )""".format(person, title))

    my_cursor.execute("""SELECT t.* FROM titles t WHERE t.title = '{}'""".format(title))
    if len(my_cursor.fetchall()) < 1:
        my_cursor.execute("INSERT INTO titles (title) VALUES ('{}')".format(title))
    myDB.commit()

    return True


def set_long_drawer(person, topic, message, chat_id):
    sql = """INSERT INTO long_drawer (person, topic, message_id, message_content, chat_id) 
            VALUES ((SELECT id FROM persons WHERE person="{}"), "{}", {}, "{}", {})
            """.format(person, topic, message.message_id, message.text, chat_id)
    my_cursor.execute(sql)
    myDB.commit()


def get_persons():
    result = []
    my_cursor.execute("SELECT person FROM persons")
    persons = my_cursor.fetchall()
    for person in persons:
        result.append(''.join(person))
    return result


def get_titles():
    result = []
    my_cursor.execute("SELECT title FROM titles")
    titles = my_cursor.fetchall()
    for title in titles:
        result.append(''.join(title))
    return result


def get_person_titles(name):
    result = []
    my_cursor.execute("""SELECT t.title FROM knights k, persons p, titles t 
                        WHERE k.person_id = p.id 
                        and k.title_id = t.id
                        and p.person = '{}'
    """.format(name))
    for title in my_cursor.fetchall():
        result.append(''.join(title))
    return result


def get_person_rank(name):
    my_cursor.execute("""SELECT t.title FROM titles t, persons p
                        WHERE t.id = p.rank_id
                        and p.person = '{}'
    """.format(name))
    return my_cursor.fetchone()[0]


def get_person_user_id(name):
    my_cursor.execute("""SELECT p.user_id FROM persons p
                        WHERE  p.person = '{}'
    """.format(name))
    return my_cursor.fetchone()[0]


def get_person_user_name(name):
    my_cursor.execute("""SELECT p.user_name_to_call FROM persons p
                        WHERE  p.person = '{}'
    """.format(name))
    return my_cursor.fetchone()[0]


def get_person_long_drawer(name, topic):
    message = collections.namedtuple('message', ['message_id', 'message_content', 'chat_id'])
    result = []
    my_cursor.execute("""SELECT l.message_id, l.message_content, l.chat_id FROM long_drawer l, persons p
                            WHERE l.person = p.id
                            and p.person = '{}' 
                            and l.topic = '{}'
        """.format(name, topic))
    for i in my_cursor.fetchall():
        result.append(message(*i))
    return result


def get_person_long_drawer_topic(name):
    result = []
    my_cursor.execute("""SELECT DISTINCT l.topic FROM long_drawer l, persons p
                                    WHERE l.person = p.id
                                    and p.person = '{}' 
                """.format(name))
    for topic in my_cursor.fetchall():
        result.append(''.join(topic))
    return result


def del_person(name):
    try:
        my_cursor.execute("DELETE FROM persons WHERE person = '{}'".format(name))
    except Exception:
        print(traceback.format_exc())


def del_title(title_name):
    try:
        my_cursor.execute("DELETE FROM titles t WHERE t.title = '{}'".format(title_name))
    except Exception:
        print(traceback.format_exc())


def del_person_title(name, title_name):
    try:
        my_cursor.execute("""DELETE FROM knights
                                WHERE knights.person_id = (SELECT id FROM persons WHERE person='{}')
                                AND knights.title_id = (SELECT id FROM titles WHERE title='{}')
                                """.format(name, title_name))
    except Exception:
        print(traceback.format_exc())


def del_person_long_drawer(name, topic, message_id):
    try:
        my_cursor.execute("""DELETE FROM long_drawer l 
                                WHERE l.person_id = (SELECT id FROM persons WHERE person='{}')
                                AND   l.topic = '{}'
                                AND   l.message_id = {}
                                """.format(name, topic, message_id))
    except Exception:
        print(traceback.format_exc())


def replace_rank(name, rank):
    try:
        my_cursor.execute("""UPDATE persons p SET p.rank_id = (SELECT id FROM titles WHERE title='{}')
                                        WHERE p.person = '{}'
                                        """.format(rank, name))
    except Exception:
        print(traceback.format_exc())
