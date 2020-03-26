# -*- coding: utf-8 -*-

import traceback
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


def set_person_call_name(person, call_name):
    sql = """INSERT INTO persons_call (person_id, call_name) VALUES ((SELECT id FROM persons WHERE person='{}'), '{}');
            """.format(person, call_name)
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


def get_person_for_call_name(call_name):
    my_cursor.execute("""SELECT person FROM persons
    INNER JOIN persons_call ON persons.id = persons_call.person_id and persons_call.call_name = '{}';
                """.format(call_name))
    result = my_cursor.fetchall()
    if len(result) > 0:
        return result[0][0]
    return False


def get_call_name_for_person(person):
    my_cursor.execute("""SELECT persons_call.call_name FROM persons
    INNER JOIN persons_call ON persons.id = persons_call.person_id and person='{}';
        """.format(person))
    result = []
    fetchall = my_cursor.fetchall()
    for call_name in fetchall:
        result.append(call_name[0])
    return result


def get_persons_call_name():
    my_cursor.execute("""SELECT person, persons_call.call_name FROM persons
    INNER JOIN persons_call ON persons.id = persons_call.person_id;""")
    fetchall = my_cursor.fetchall()
    result = {}
    for person, call_name in fetchall:
        try:
            result.update({person: result.get(person) + [call_name]})
        except TypeError:
            result.update({person: [call_name]})
    return result


def del_person(name):
    try:
        my_cursor.execute("DELETE FROM persons WHERE person = '{}'".format(name))
        myDB.commit()
    except Exception:
        print(traceback.format_exc())


def del_title(title_name):
    try:
        my_cursor.execute("DELETE FROM titles  WHERE titles.title = '{}'".format(title_name))
        myDB.commit()
    except Exception:
        print(traceback.format_exc())


def del_person_title(name, title_name):
    try:
        my_cursor.execute("""DELETE FROM knights
                                WHERE knights.person_id = (SELECT id FROM persons WHERE person='{}')
                                AND knights.title_id = (SELECT id FROM titles WHERE title='{}')
                                """.format(name, title_name))
        myDB.commit()
    except Exception:
        print(traceback.format_exc())


def del_person_call_name(call_name):
    try:
        my_cursor.execute("""DELETE FROM persons_call
                                WHERE persons_call.call_name = '{}'""".format(call_name))
        myDB.commit()
    except Exception:
        print(traceback.format_exc())


def replace_rank(name, rank):
    try:
        my_cursor.execute("""UPDATE persons SET rank_id = (SELECT id FROM titles WHERE title='{}')
                                        WHERE person = '{}'
                                        """.format(rank, name))
        myDB.commit()
    except Exception:
        print(traceback.format_exc())
