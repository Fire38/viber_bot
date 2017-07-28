import psycopg2
import datetime
from viber_bot.settings import DATABASES


class Middleware():
    def __init__(self):
        db_info = DATABASES.get('default')
        self.con = psycopg2.connect(database=db_info.get('NAME'),
                                    user=db_info.get('USER'),
                                    password=db_info.get('PASSWORD'),
                                    host=db_info.get('HOST'),
                                    port=db_info.get('PORT')
                                    )

        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS statistic (id serial PRIMARY KEY, username text, chat_id text, "
                            "course text, groupa text, choice text, date timestamp not null default 'epoch', messager text)")
        self.con.commit()

    def get_user(self, username, chat_id, messager):
        """Добавляет пользоввателя в таблицу statistic"""
        self.username = username
        self.chat_id = chat_id
        self.request_datetime = datetime.datetime.now()
        self.messager = messager
        self.cursor.execute("INSERT INTO statistic (username, chat_id, course, groupa, choice, date, messager) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (self.username, self.chat_id, "empty", "empty", "empty", self.request_datetime, self.messager))
        self.con.commit()

    def update_group(self, chat_id, groupa):
        """Обновляет запись в statistic добавляя группу"""
        self.chat_id = chat_id
        self.groupa = groupa
        print(self.chat_id, self.groupa)
        self.cursor.execute("UPDATE statistic SET groupa = (%s) WHERE id IN (SELECT max(id) FROM statistic"
                            " WHERE chat_id = (%s) AND course = (%s))", (self.groupa, self.chat_id, "empty"))
        self.con.commit()

    def update_course(self, chat_id, course):
        """Обновляем курс"""
        self.chat_id = chat_id
        self.course = course
        print(self.chat_id, self.course)
        self.cursor.execute("UPDATE statistic SET course = (%s) WHERE id IN (SELECT max(id) FROM statistic"
                            " WHERE chat_id = (%s))", (self.course, self.chat_id))
        self.con.commit()

    def get_full_info(self, chat_id):
        """Возвращает данные для запроса к таблице с расписанием"""
        self.chat_id = chat_id

        self.cursor.execute("SELECT * FROM statistic WHERE id IN (SELECT max(id) FROM statistic"
                            " WHERE chat_id = (%s) AND choice = (%s) AND choice != (%s) AND choice != (%s))",
                            (self.chat_id, "empty", "time", "subscribe"))
        return self.cursor.fetchone()

    def add_time(self, username, chat_id, messager):
        """Добавляет в статистику запись о запросе времени пар"""
        self.username = username
        self.chat_id = chat_id
        self.choice = "time"
        self.request_datetime = datetime.datetime.now()
        self.messager = messager

        self.cursor.execute("INSERT INTO statistic (username, chat_id, course, groupa, choice, date, messager)"
                            " VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (self.username, self.chat_id, "empty", "empty", self.choice, self.request_datetime, self.messager))
        self.con.commit()

    def add_subscribe(self, username, chat_id, choice, messager):
        """Добавляет в статистику запись о запросе расписания по подписке"""
        self.username = username
        self.chat_id = chat_id
        self.choice = choice
        self.messager = messager
        self.request_datetime = datetime.datetime.now()

        self.cursor.execute("SELECT * FROM subscribers WHERE chat_id = (%s)", (self.chat_id,))
        user = self.cursor.fetchone()
        if user:
            self.course, self.groupa = user[3:]
            self.cursor.execute("INSERT INTO statistic (username, chat_id, course, groupa, choice, date, messager)"
                                " VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (self.username, self.chat_id, self.course, self.groupa, self.choice, self.request_datetime, self.messager))
            self.con.commit()
            return True
        else:
            return False
