import django_filters
from django import forms

from vbot.models import Raspisanie


class ScheduleFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super(ScheduleFilter, self).__init__(*args, **kwargs)
        self.filters['group'].label = 'Группа'

    class Meta:
        model = Raspisanie
        fields = ['group', 'course',]
