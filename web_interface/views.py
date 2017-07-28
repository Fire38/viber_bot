from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .filters import ScheduleFilter
from vbot.models import UserProfile
from vbot.models import Raspisanie, Group, Subject, Teacher
from .forms import GroupForm, SubjectGroup, TeacherForm, ScheduleForm, UserProfileForm, ChangePasswordForm


# Create your views here.

def auth(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    error = False
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Ваша учетная записать не активирована:(')
        else:
            error = True
    return render(request, 'web_interface/auth.html', {'error': error})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth'))


@login_required
def index(request):
    schedule = Raspisanie.objects.all()
    schedule_filter = ScheduleFilter(request.GET, queryset=schedule)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return render(request, 'web_interface/index.html', {'filter': schedule_filter,
                                                        'user_profile': user_profile
                                                        })


@login_required
def groups(request):
    all_groups = Group.objects.all().order_by('name')
    form = GroupForm()
    return render(request, 'web_interface/groups.html', {'groups': all_groups,
                                                         'form': form
                                                         })


@login_required
def subjects(request):
    all_subjects = Subject.objects.all().order_by('title')
    form = SubjectGroup()
    return render(request, 'web_interface/subjects.html', {'subjects': all_subjects,
                                                           'form': form
                                                           })


@login_required
def teachers(request):
    all_teacher = Teacher.objects.all().order_by('name')
    form = TeacherForm()
    return render(request, 'web_interface/teachers.html', {'teachers': all_teacher,
                                                           'form': form
                                                           })


@login_required
def schedule(request):
    adding = False
    exist = False
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            adding = True
        # если запись дублируется
        else:
            exist = True
    form = ScheduleForm()
    return render(request, 'web_interface/add_schedule.html', {'form': form,
                                                               'adding': adding,
                                                               'exist': exist
                                                               })


@login_required
def setting(request):
    profile_form = UserProfileForm()
    change_password_form = ChangePasswordForm()
    return render(request, 'web_interface/settings.html', {'profile_form': profile_form,
                                                           'change_password_form': change_password_form
                                                           })


def change_avatar(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    # Заполняем форму тем что пришло в post запросе
    profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        # указали чей это профиль
        profile.user = request.user
        if 'picture' in request.FILES:
            profile.picture = request.FILES['picture']
        profile.save()
        return HttpResponseRedirect(reverse('index'))


def change_password(request):
    success = False
    error = False
    old_pass = request.POST['old_password']
    new_pass1 = request.POST['new_password1']
    new_pass2 = request.POST['new_password2']
    user = User.objects.get(username=request.user)
    if old_pass == new_pass1:
        error = True
    elif user.check_password(old_pass) and new_pass1 == new_pass2:
        user.set_password(new_pass1)
        user.save()
        success = True
    return render(request, 'web_interface/settings.html', {'success': success,
                                                           'error': error,
                                                           'profile_form': UserProfileForm(),
                                                           'change_password_form': ChangePasswordForm()
                                                           })




