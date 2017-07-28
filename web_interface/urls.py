from django.conf.urls import url

from .views import *
from .ajax_requests import delete_schedule, add_elements_to_database

urlpatterns = [
    url(r'^auth/$', auth, name='auth'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^index/$', index, name='index'),
    url(r'^groups/$', groups, name='groups'),
    url(r'^subjects/$', subjects, name='subjects'),
    url(r'^teachers/$', teachers, name='teachers'),
    url(r'^add_schedule/$', schedule, name='schedule'),
    url(r'^settings/$', setting, name='settings'),
    url(r'^change_avatar', change_avatar, name='change_avatar'),
    url(r'change_password', change_password, name='change_password'),

    url(r'^ajax/add/', add_elements_to_database, name='add_elements_to_database'),
    url(r'^ajax/delete_schedule/', delete_schedule, name='delete_schedule')
]


