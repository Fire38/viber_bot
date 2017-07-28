import psycopg2
import datetime
from viber_bot.settings import DATABASES

class Subscriber():
    def __init__(self):
        db_info = DATABASES.get('default')
        self.con = psycopg2.connect(
            database=db_info.get('NAME'),
            user=db_info.get('USER'),
            password=db_info.get('PASSWORD'),
            host=db_info.get('HOST'),
            port=db_info.get('PORT')
        )
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS subscribers (id serial PRIMARY KEY, username text, chat_id text, course text, groupa text)")
        self.con.commit()

    def add_subscriber(self, data):
        self.data = data
        self.datetime_request = datetime.datetime.now()
        self.cursor.execute("SELECT * FROM subscribers WHERE chat_id = (%s)", (self.data[2],))
        # Если такая запись существует, то подписка ПЕРЕоформляется
        if self.cursor.fetchone() is not None:
            # Добавили в подписчики
            self.cursor.execute("UPDATE subscribers SET course = (%s), groupa = (%s) WHERE chat_id = (%s)", (self.data[3], self.data[4], self.data[2]))
            # Добавили в статистику
            self.cursor.execute("INSERT INTO statistic (username, chat_id, course, groupa, choice, date, messager) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (self.data[1], self.data[2], self.data[3], self.data[4], 'subscribe', self.datetime_request, self.data[7]))
            # И удаляем запись, которая добавляется при запросе расписания
            self.cursor.execute("DELETE FROM statistic WHERE id IN ( SELECT max(id) FROM statistic WHERE chat_id = (%s) AND choice='empty')", (self.data[2],))
            self.con.commit()
            return "Подписка переоформлена на группу %s, %s" % (self.data[4], self.data[3])

        else:
            self.cursor.execute("INSERT INTO subscribers (username, chat_id, course, groupa) VALUES (%s, %s, %s, %s)", (self.data[1], self.data[2], self.data[3], self.data[4]))
            self.cursor.execute("INSERT INTO statistic (username, chat_id, course, groupa, choice, date, messager) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (self.data[1], self.data[2], self.data[3], self.data[4], 'subscribe', self.datetime_request, self.data[7]))
            self.cursor.execute("DELETE FROM statistic WHERE id IN ( SELECT max(id) FROM statistic WHERE chat_id = (%s) AND choice='empty')", (self.data[2],))
            self.con.commit()
            return "Подписка оформлена на группу %s, %s" % (self.data[4], self.data[3])