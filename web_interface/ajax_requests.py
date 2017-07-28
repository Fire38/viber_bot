from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from vbot.models import Raspisanie, Group, Subject, Teacher

querysets = {'group': Group,
             'teacher': Teacher,
             'subject': Subject
             }

@csrf_exempt
def add_elements_to_database(request):
    """Функция добавляет или удаляет записи таблицы в зависимости от пришедшего типа"""
    type = request.POST.get('type')
    name = request.POST.get('name')
    value = request.POST.get('value', None)
    # добавление на страницах группы/препода/предмета
    if type == 'add' and value.strip():
        # в одной таблице не name, а title
        try:
            object, created = querysets[name].objects.get_or_create(name=value.strip())
            html = '<tr><td><input type="checkbox" name="check" value="' + str(object.id)+'" /></td><td>' + object.name + '</td></tr>'
            data = {'created': created, 'id': object.id, 'name': object.name, 'html': html}
        except:
            object, created = Subject.objects.get_or_create(title=value.strip())
            html = '<tr><td><input type="checkbox" name="check" value="' + str(object.id)+'" /></td><td>' + object.title + '</td></tr>'
            data = {'created': created, 'id': object.id, 'name': object.title, 'html': html}
        return JsonResponse(data)
    # добавление на странице создания расписания
    elif type == 'dynamic_add' and value.strip():
        try:
            object, created = querysets[name].objects.get_or_create(name=value.strip())
            html = '<option value="' + str(object.id) + '" selected="selected"> ' + str(object.name) + '</option>'
            data = {'created': created, 'id': object.id, 'name': object.name, 'html': html}
        except:
            object, created = Subject.objects.get_or_create(title=value.strip())
            html = '<option value="' + str(object.id) + '" selected="selected"> ' + str(object.title) + '</option>'
            data = {'created': created, 'id': object.id, 'name': object.title, 'html': html}
        return JsonResponse(data)

    elif type == 'delete':
        elements = request.POST.getlist('id[]')
        querysets[name].objects.filter(id__in=elements).delete()
        return JsonResponse({'error': True, 'created': False})

    else:
        data = {'error': True, 'created': False}
        return JsonResponse(data)


def delete_schedule(request):
    elements = request.GET.getlist('id[]')
    Raspisanie.objects.filter(id__in=elements).delete()
    return JsonResponse({'error': True, 'created': False})


