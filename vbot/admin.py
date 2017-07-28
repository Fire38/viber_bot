from django.contrib import admin
from .models import Teacher, Subject, Raspisanie, Group, UserProfile

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Raspisanie)
admin.site.register(Group)
admin.site.register(UserProfile)
