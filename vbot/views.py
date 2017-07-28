from django.http import JsonResponse
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from viberbot import Api
from viberbot.api.messages import KeyboardMessage
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.messages.sticker_message import StickerMessage

import datetime
from decouple import config

from .keyboard import *
from .subscribe import Subscriber
from .middleware import Middleware
from .back_button import BackButton
from .db_request import DatabaseRequest
from .show_schedule import show, show_for_subscriber


bot_configuration = BotConfiguration(
    name='Робот',
    avatar='http://brstu.ru/docs/faculties/feiu/feiu-logo.jpg',
    auth_token=config('TOKEN')
)
viber = Api(bot_configuration)

middleware = Middleware()
db_request = DatabaseRequest()
back_button = BackButton()
subscriber = Subscriber()


@csrf_exempt
def index(request):
    req = request.body
    viber_request = viber.parse_request(req.decode('utf-8'))

    if isinstance(viber_request, ViberMessageRequest):
        username = viber_request.sender.name
        chat_id = viber_request.sender.id
        request_text = viber_request.message.text

        if request_text == "Меню":
            viber.send_messages(chat_id, [TextMessage(text='Выберите пункт меню')])
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=MAIN_MENU)])

        elif request_text == "Получить расписание по подписке":
            success_adding = middleware.add_subscribe(username, chat_id, 'get_subscribe', 'Viber')
            if success_adding:
                schedule = db_request.get_subscribers_schedule(chat_id)
                if schedule:
                    today_sch, tomorrow_sch = show_for_subscriber(schedule)
                    try:
                        today_date = datetime.datetime.today().strftime('%d.%m')
                        viber.send_messages(chat_id, [TextMessage(text="Расписание на сегодня (" + today_date + "):\n\n" + today_sch)])
                    except:
                        viber.send_messages(chat_id, [TextMessage(text="Запрос не удалось обработать, попробуйте позже")])

                    try:
                        tomorrow_date = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d.%m')
                        viber.send_messages(chat_id, [TextMessage(text="Расписание на завтра (" + tomorrow_date + "):\n\n" + tomorrow_sch)])
                    except:
                        viber.send_messages(chat_id, [TextMessage(text="Запрос не удалось обработать, попробуйте позже")])
                else:
                    viber.send_messages(chat_id, [TextMessage(text="Запрос не выполнен")])
            else:
                viber.send_messages(chat_id, [TextMessage(text="Вы еще не подписаны на расписание")])
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=MAIN_MENU)])

        elif request_text == "Время пар":
            middleware.add_time(username, chat_id, "Viber")
            viber.send_messages(chat_id, [TextMessage(text=render_to_string('time.md'))])
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=MAIN_MENU)])

        elif request_text == "Получить расписание":
            # добавляем пользователя в статистику, курс, специальность и дата запроса - empty
            middleware.get_user(username, chat_id, "Viber")
            viber.send_messages(chat_id, [TextMessage(text="Выберите специальность")])
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=SELECT_GROUP)])

        elif request_text == "ПИЭ" or request_text == "УП" or\
                request_text == "ГМУ" or request_text == "ИМ" or\
                request_text == "УИ" or request_text == "ФиК" or\
                request_text == "ПМ" or request_text == "К":
            middleware.update_group(chat_id, request_text)
            viber.send_messages(chat_id, [TextMessage(text="Выберите курс")])
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=SELECT_COURSE)])

        elif request_text == "1 курс" or request_text == "2 курс" \
                or request_text == "3 курс" or request_text == "4 курс":
            middleware.update_course(chat_id, request_text)
            viber.send_messages(chat_id, [TextMessage(text="Выберите время")])
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=FINAL_MENU)])

        # todo На сегодня и на завтра похожи, мб функция?
        elif request_text == "На сегодня":
            data = middleware.get_full_info(chat_id)
            course = data[3]
            group = data[4]
            # запрос расписания, курс берем только цифру
            schedule = db_request.get_today_schedule(course[0], group)
            try:
                viber.send_messages(chat_id, [TextMessage(text=show(schedule))])
            except:
                viber.send_messages(chat_id, [TextMessage(text="Запрос не удалось обработать, попробуйте позже")])
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=MAIN_MENU)])

        elif request_text == "На завтра":
            data = middleware.get_full_info(chat_id)
            course = data[3]
            group = data[4]
            schedule = db_request.get_tomorrow_schedule(course[0], group)
            try:
                viber.send_messages(chat_id, [TextMessage(text=show(schedule))])
            except:
                viber.send_messages(chat_id, [TextMessage(text="Запрос не удалось обработать, попробуйте позже")])
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=MAIN_MENU)])

        elif request_text == "На главную":
            back_button.cancel_operation(chat_id, 0)
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=MAIN_MENU)])

        elif request_text == "Вернуться назад":
            empty_count = db_request.select_backbutton(chat_id)
            if empty_count == 1:
                back_button.cancel_operation(chat_id, 1)
                viber.send_messages(chat_id, [KeyboardMessage(keyboard=SELECT_COURSE)])
            elif empty_count == 2:
                back_button.cancel_operation(chat_id, 2)
                viber.send_messages(chat_id, [KeyboardMessage(keyboard=SELECT_GROUP)])
            elif empty_count == 3:
                back_button.cancel_operation(chat_id, 0)
                viber.send_messages(chat_id, [KeyboardMessage(keyboard=MAIN_MENU)])

        elif request_text == "Подписаться на это расписание":
            data = middleware.get_full_info(chat_id)
            response = subscriber.add_subscriber(data)
            viber.send_messages(chat_id, [TextMessage(text=response)])
            viber.send_messages(chat_id, [KeyboardMessage(keyboard=MAIN_MENU)])
    else:
        viber.send_messages(viber_request.sender.id, [StickerMessage(sticker_id=40133)])
        viber.send_messages(viber_request.sender.id, [TextMessage(text="Что-то не так, попробуйте еще раз")])
    return JsonResponse({}, status=200)





#Пример запроса
"""
ViberMessageRequest
[event_type=message,
timestamp=1498799862283,
message_token=5061443159342451146,
sender=UserProfile[name=Роман Саблин, avatar=https://media-direct.cdn.viber.com/download_photo?dlid=0lmYu0BW8EnttzNGSiHnww_XAnU_9PkaIx90Dgkdc6VKhOuEi6jp4fKPIxpG2WH7O1goyiLdETrSR0A1q1ihBTqhloL5p34PgxVc4tjldbmguMQ5_n5bgKV36lMnFJriHtKXOQ&fltp=jpg&imsz=0000,
                                                                                                                                                                                                                                                         id=nT7x1IzZ3XbEpRjBs7pY+g==, country=RU, language=ru, api_version=2, message=TextMessage [tracking_data=None, keyboard=None, min_api_version=None, text=A], chat_id=None, reply_type=None, silent=False]
"""