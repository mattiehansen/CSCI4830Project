from django.shortcuts import render
from django.contrib import messages
from .models import CustomUser, Student, Teacher, Pass
from .forms import LoginForm, PassForm, ReturnForm, UserForm, StudentForm, TeacherForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST


def index(request):
    form = LoginForm
    return render(request, 'schoolpass/index.html')


# @require_POST
def pagetwo(request):
    form = PassForm
    return render(request, 'schoolpass/pagetwo.html')


# @require_POST
def pagethree(request):
    form = ReturnForm
    return render(request, 'schoolpass/pagethree.html')


# @require_POST
def rejected(request):
    return render(request, 'schoolpass/rejected.html')


# @require_POST
def returned(request):
    return render(request, 'schoolpass/returned.html')


def student_registration(request):
    user_form = UserForm(request.POST or None, prefix='UF')
    profile_form = StudentForm(request.POST or None, prefix='PF')
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save(commit=False)
        user.is_student = True
        user.save()
        user.student_profile.classes_enrolled = profile_form.cleaned_data.get('classes_enrolled')
        user.student_profile.accommodations = profile_form.cleaned_data.get('accommodations')
        user.student_profile.notes = profile_form.cleaned_data.get('notes')
        user.student_profile.save()
        messages.success(request, "Student was successfully created!")

    return render(request, 'schoolpass/studentregistration.html',
                  {'user_form': user_form, 'profile_form': profile_form,})


def teacher_registration(request):
    user_form = UserForm(request.POST or None, prefix='UF')
    profile_form = TeacherForm(request.POST or None, prefix='PF')
    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save(commit=False)
        user.is_teacher = True
        user.save()
        user.teacher_profile.classes_taught = profile_form.cleaned_data.get('classes_taught')
        user.teacher_profile.room_number = profile_form.cleaned_data.get('room_number')
        user.teacher_profile.save()
        messages.success(request, "Teacher Successfully Created")

    return render(request, 'schoolpass/teacherregistration.html',
                  {'user_form': user_form, 'profile_form': profile_form, })
