from django.db import models
from django.contrib.auth.models import User

# Create your models here.
SUBGROUP_CHOICES = (
    ('1', '1'),
    ('2', '2')
)

COURSE_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4')
)

SUBJECT_TYPE_CHOICES = (
    ('лекция', 'лекция'),
    ('практика', 'практика'),
    ('лабораторная', 'лабораторная')
)

WEEKDAY_CHOICES = (
    (0, 'Понедельник'),
    (1, 'Вторник'),
    (2, 'Среда'),
    (3, 'Четверг'),
    (4, 'Пятница'),
    (5, 'Суббота'),
    (6, 'Воскресенье')
)

TYPE_OF_WEEK_CHOICES = (
    ('Верхняя', 'Верхняя'),
    ('Нижняя', 'Нижняя'),
    ('Верхняя и нижняя', 'Верхняя и нижняя')
)

TIME_CHOICES = (
    ('8:15', '8:15'),
    ('10:00', '10:00'),
    ('11:45', '11:45'),
    ('13:30', '13:30'),
    ('15:15', '15:15'),
    ('17:00', '17:00'),
    ('18:45', '18:45')
)

class Group(models.Model):
    name = models.CharField("Название группы", max_length=15, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField("ФИО", max_length=50, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    title = models.CharField("Название", max_length=70, unique=True)

    def __str__(self):
        return self.title


class Raspisanie(models.Model):
    subject = models.ForeignKey(Subject)
    teacher = models.ForeignKey(Teacher, blank=True, null=True, default=0)
    group = models.ForeignKey(Group)
    classroom = models.CharField("Номер аудитории", max_length=4, blank=True, default=0000)
    subgroup = models.CharField("Номер подгруппы", max_length=2, choices=SUBGROUP_CHOICES, blank=True)
    course = models.CharField("Курс", max_length=2, choices=COURSE_CHOICES, default=1)
    subject_type = models.CharField("Тип пары", max_length=20, choices=SUBJECT_TYPE_CHOICES, default=1)
    weekday = models.IntegerField("День недели", choices=WEEKDAY_CHOICES, default=0)
    type_of_week = models.CharField("Тип недели", choices=TYPE_OF_WEEK_CHOICES, default=1, max_length=20)
    time = models.CharField("Время начала", choices=TIME_CHOICES, default=1, max_length=10)

    def __str__(self):
        self.information = str(WEEKDAY_CHOICES[self.weekday][1]) + " " + str(self.group) + " " + str(self.subject) + " " + str(self.type_of_week)
        return self.information

    class Meta:
        unique_together = ('subject', 'teacher', 'group', 'classroom', 'subgroup', 'course', 'subject_type', 'weekday', 'type_of_week', 'time')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
