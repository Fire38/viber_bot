import psycopg2
import datetime
from viber_bot.settings import DATABASES


class DatabaseRequest():
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

    def select_backbutton(self, chat_id):
        """Находит последний запрос пользователя в statistic, считает количество empty и возвращает это число"""
        self.chat_id = chat_id
        empty_list = []
        self.cursor.execute("SELECT * FROM statistic WHERE id IN (SELECT max(id) FROM statistic "
                            "WHERE chat_id = (%s) AND choice != (%s) AND choice != (%s))", (self.chat_id, "time", "subscribe"))
        for i, e in enumerate(self.cursor.fetchone()):
            if e == "empty":
                empty_list.append(e)
        return len(empty_list)

    def get_today_schedule(self, course, groupa):
        """Возвращает расписание на сегодня"""
        self.course = course
        self.groupa = groupa
        today = datetime.datetime.today().weekday()
        # Верхняя или нижняя неделя
        if datetime.datetime.now().isocalendar()[1] % 2 == 0:
            self.type = "Нижняя"
        else:
            self.type = "Верхняя"

        self.cursor.execute("SELECT vr.time, vs.title, vr.subject_type, vt.name, vr.classroom\
                            FROM vbot_raspisanie AS vr\
                            JOIN vbot_subject AS vs ON (vr.subject_id = vs.id)\
                            JOIN vbot_teacher AS vt ON (COALESCE(vr.teacher_id, '1') = vt.id)\
                            JOIN vbot_group AS vg ON (vr.group_id = vg.id)\
                            WHERE vr.type_of_week IN ('Верхняя и нижняя', (%s))\
                            AND vr.course = (%s)\
                            AND vg.id = (SELECT id FROM vbot_group WHERE name = (%s))\
                            AND vr.weekday = (%s) ORDER BY vr.time", (self.type, self.course[0], self.groupa, today)
                            )
        return self.cursor.fetchall()

    def get_tomorrow_schedule(self, course, groupa):
        """Возвращает расписание на завтра"""
        self.course = course
        self.groupa = groupa
        tomorrow = datetime.datetime.today().weekday()
        if tomorrow == 5 or tomorrow == 6:
            tomorrow = 0
        else:
            tomorrow += 1
        # Верхняя или нижняя
        if datetime.datetime.now().isocalendar()[1] % 2 == 0:
            self.type = "Нижняя"
        else:
            self.type = "Верхняя"
        self.cursor.execute("SELECT vr.time, vs.title, vr.subject_type, vt.name, vr.classroom\
                            FROM vbot_raspisanie AS vr\
                            JOIN vbot_subject AS vs ON (vr.subject_id = vs.id)\
                            JOIN vbot_teacher AS vt ON (COALESCE(vr.teacher_id, '1') = vt.id)\
                            JOIN vbot_group AS vg ON (vr.group_id = vg.id)\
                            WHERE vr.type_of_week IN ('Верхняя и нижняя', (%s))\
                            AND vr.course = (%s)\
                            AND vg.id = (SELECT id FROM vbot_group WHERE name = (%s))\
                            AND vr.weekday = (%s) ORDER BY vr.time", (self.type, self.course[0], self.groupa, tomorrow)
                            )
        return self.cursor.fetchall()

    def get_subscribers_schedule(self, chat_id):
        """Возвращает расписание для подписчиков на сегодня и завтра"""
        self.chat_id = chat_id
        self.cursor.execute("SELECT * FROM subscribers WHERE chat_id = (%s)", (self.chat_id,))
        subscriber_data = self.cursor.fetchone()
        if subscriber_data is not None:
            self.course = subscriber_data[3]
            self.groupa = subscriber_data[4]
            today = datetime.datetime.today().weekday()
            tomorrow = datetime.datetime.today().weekday()
            # Если завтра воскресенье - выдаем расписание на понедельник
            if tomorrow == 6:
                tomorrow = 0
            else:
                tomorrow += 1
            # Верхняя или нижняя неделя
            if datetime.datetime.now().isocalendar()[1] % 2 == 0:
                self.type = "Нижняя"
            else:
                self.type = "Верхняя"

            self.cursor.execute("SELECT vr.time, vs.title, vr.subject_type, vt.name, vr.classroom\
                                       FROM vbot_raspisanie AS vr\
                                       JOIN vbot_subject AS vs ON (vr.subject_id = vs.id)\
                                       JOIN vbot_teacher AS vt ON (COALESCE(vr.teacher_id, '1') = vt.id)\
                                       JOIN vbot_group AS vg ON (vr.group_id = vg.id)\
                                       WHERE vr.type_of_week IN ('Верхняя и нижняя', (%s))\
                                       AND vr.course = (%s)\
                                       AND vg.id = (SELECT id FROM vbot_group WHERE name = (%s))\
                                       AND vr.weekday = (%s) ORDER BY vr.time",
                                (self.type, self.course[0], self.groupa, today)
                                )
            today_schedule = self.cursor.fetchall()

            self.cursor.execute("SELECT vr.time, vs.title, vr.subject_type, vt.name, vr.classroom\
                                        FROM vbot_raspisanie AS vr\
                                        JOIN vbot_subject AS vs ON (vr.subject_id = vs.id)\
                                        JOIN vbot_teacher AS vt ON (COALESCE(vr.teacher_id, '1') = vt.id)\
                                        JOIN vbot_group AS vg ON (vr.group_id = vg.id)\
                                        WHERE vr.type_of_week IN ('Верхняя и нижняя', (%s))\
                                        AND vr.course = (%s)\
                                        AND vg.id = (SELECT id FROM vbot_group WHERE name = (%s))\
                                        AND vr.weekday = (%s) ORDER BY vr.time",
                                (self.type, self.course[0], self.groupa, tomorrow)
                                )

            tomorrow_schedule = self.cursor.fetchall()
            schedules = [today_schedule, tomorrow_schedule]
            return schedules
        else:
            return False
