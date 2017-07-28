"""Функции для отображения расписания"""


def show(data):
    string = ''
    print(data)
    if len(data) > 0:
        for para in data:
            time, subject, type, teacher, classroom = para
            string += time + " - " + subject + "/" + type + "/" + teacher + "/ауд." + classroom + "\n\n"
    else:
        string = "Пар нет"
    return string.rstrip()

def show_for_subscriber(data):
    massiv = []
    for spisok in data:
        string = ''
        if len(spisok) > 0:
            for para in spisok:
                time, subject, type, teacher, classroom = para
                string += time + " - " + subject + "/" + type + "/" + teacher + "/ауд." + classroom + "\n\n"
        else:
            string = "Пар нет"
        massiv.append(string.rstrip())
    return massiv


