from django import forms
from django.forms import ModelForm

from vbot.models import Group, Subject, Teacher, Raspisanie, UserProfile


class GroupForm(ModelForm):
    name = forms.CharField(label='Название группы', max_length=10, required=False)

    class Meta:
        model = Group
        fields = ['name']


class SubjectGroup(ModelForm):
    title = forms.CharField(label='Название предмета',  widget=forms.TextInput(attrs={'id': 'id_name', 'class': 'clearable'}),
                            max_length=70, required=False)

    class Meta:
        model = Subject
        fields = ['title']


class TeacherForm(ModelForm):
    name = forms.CharField(label='ФИО преподавателя', max_length=50, required=False)

    class Meta:
        model = Teacher
        fields = ['name']


class ScheduleForm(ModelForm):
    subject = forms.ModelChoiceField(label='Предмет', queryset=Subject.objects.all().order_by('title'))
    teacher = forms.ModelChoiceField(label='Преподаватель', queryset=Teacher.objects.all().order_by('name'), required=False)
    group = forms.ModelChoiceField(label='Группа', queryset=Group.objects.all().order_by('name'))

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.all().order_by('title')

    class Meta:
        model = Raspisanie
        fields = ['subject', 'teacher', 'group', 'course', 'subgroup', 'classroom', 'subject_type', 'weekday',
                  'type_of_week', 'time']


class UserProfileForm(ModelForm):
    picture = forms.ImageField(label='')

    class Meta:
        model = UserProfile
        fields = ['picture']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)



