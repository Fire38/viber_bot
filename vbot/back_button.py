import psycopg2
from viber_bot.settings import DATABASES


class BackButton():
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

    def cancel_all(self, chat_id):
        self.chat_id = chat_id
        self.cursor.execute("DELETE FROM statistic WHERE id IN (SELECT max(id) FROM statistic "
                            "WHERE chat_id = (%s))", (self.chat_id,))
        self.con.commit()

    def cancel_groupa(self, chat_id):
        self.chat_id = chat_id
        self.cursor.execute("UPDATE statistic SET groupa = (%s) WHERE id IN (SELECT max(id) FROM statistic "
                            "WHERE chat_id = (%s) AND course = (%s))", ("empty", self.chat_id, "empty"))
        self.con.commit()

    def cancel_course(self, chat_id):
        self.chat_id = chat_id
        self.cursor.execute("UPDATE statistic SET course = (%s) WHERE id IN (SELECT max(id) FROM statistic"
                            " WHERE chat_id = (%s) AND groupa != (%s))", ("empty", self.chat_id, "epmty"))
        self.con.commit()
    
    def cancel_operation(self, chat_id, empty_count):
        """В соответствии с количеством пустых полей выбирает какой метод выполнять"""
        self.chat_id = chat_id
        self.empty_count = empty_count
        if self.empty_count == 1:
            self.cancel_course(self.chat_id)
        elif self.empty_count == 2:
            self.cancel_groupa(self.chat_id)
        elif self.empty_count == 0:
            self.cancel_all(self.chat_id)
