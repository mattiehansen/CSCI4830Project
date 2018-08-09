from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Student, Teacher, Pass
from .forms import PassForm, ReturnForm, UserForm, StudentForm, TeacherForm
from .decorators import student_required, teacher_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test


def index(request):
    """
    Views for the index page.
    For logged in users:
        Admins are redirected to registrations forms (AKA admin panel) page.
        Students are redirected to school pass app page.

    :param request:
    :return: index, pagetwo, or registration_forms pages
    """
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('pagetwo')
        elif request.user.is_superuser:
            return redirect('registration_forms')
        else:
            return redirect('logout')
    return render(request, 'schoolpass/index.html')


"""

Pass app views/pages.

"""


@login_required
@student_required
def pagetwo(request):
    form = PassForm
    return render(request, 'schoolpass/pagetwo.html', {'form': form})


@login_required
@student_required
@require_POST
def process_pass(request):
    form = PassForm(request.POST)
    if form.is_valid():
        description = form.cleaned_data['description']
        teacher_username = form.cleaned_data['teacher_username']
        teacher_password = form.cleaned_data['teacher_password']
        try:
            teacher_user = CustomUser.objects.get(username=teacher_username)
        except:
            return redirect('pagetwo')
        if teacher_user.is_teacher and teacher_user.check_password(teacher_password) and teacher_user.is_staff:
            if 'Accept' in request.POST:
                '''
                create and link to pass here, pass variables
                '''
                user = CustomUser.objects.get(id=request.user.id)
                user.pass_attempts += 1
                user.save()
                return redirect('pagetwo')# Change to page three!!!!!
                #return redirect('pagethree')
            else:  # if pass is rejected, log out student, redirect to index
                user = CustomUser.objects.get(id=request.user.id)
                user.pass_attempts += 1
                user.pass_rejections += 1
                user.save()
                logout(request)
                return redirect('index')
        else:  # if invalid username or password, redirect to same page
            return redirect('pagetwo')


@login_required
@student_required
def pagethree(request, pk):
    """
    Page of a school pass. Where and when students do and complete their pass.
    They would show this page to a teacher when returned.
    :param request:
    :param pk: id of the pass
    :return: log out and redirect to home page if complete, redirect to itself otherwise
    """
    school_pass = Pass.objects.get(id=pk)
    form = ReturnForm(request.POST or None)
    if form.is_valid():
        teacher_username = form.cleaned_data['teacher_username']
        teacher_password = form.cleaned_data['teacher_password']
        try:
            teacher_user = CustomUser.objects.get(username=teacher_username)
        except:
            return redirect('pagethree', pk=pk)
        if teacher_user.is_teacher and teacher_user.check_password(teacher_password) and teacher_user.is_staff:
            school_pass.time_returned = datetime.now()
            school_pass.save()
            logout(request)
            return redirect('index')
        else: # if invalid username or password, redirect to same page
            return redirect('pagethree', pk=pk)
    return render(request, 'schoolpass/pagethree.html', {'form': form, 'school_pass': school_pass})


@login_required
@student_required
def rejected(request):
    return render(request, 'schoolpass/rejected.html')


@login_required
@student_required
def returned(request):
    return render(request, 'schoolpass/returned.html')


"""
End pass app views/pages.

"""


"""

Superuser/admin only views/pages

"""


@user_passes_test(lambda u: u.is_superuser)
def registration_forms(request):
    """
    The registration forms page where admins create student and teacher user accounts.
    Link to the admin site is also included where account fields can be edited.
    DO NOT USE ADMIN SITE'S USER, STUDENT, AND TEACHER CREATION PAGES TO CREATE ACCOUNTS!
    USE FORMS ON THIS PAGE INSTEAD! OTHERWISE ACCOUNTS WOULD NOT WORK PROPERLY!
    FIELDS CAN BE EDITED ON ADMIN SITE ONCE ACCOUNTS CREATED ON THEIR RESPECTIVE FORMS!
    :param request:
    :return: render(request, 'schoolpass/registration_forms.html')
    """
    return render(request, 'schoolpass/registration_forms.html')


@user_passes_test(lambda u: u.is_superuser)
def student_registration(request):
    """"
    The student registration page where admins create student user accounts.
    DO NOT USE ADMIN SITE'S USER AND STUDENT CREATION PAGES!
    USE THIS FORM INSTEAD TO CREATE STUDENTS!
    Credit to Nipun Brahmbhatt:
    https://blog.botreetechnologies.com/supporting-multiple-roles-using-djangos-user-model-62afa9ce6f61
    :param request:
    :return: student registration page and forms.
    """
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


@user_passes_test(lambda u: u.is_superuser)
def teacher_registration(request):
    """"
    The student registration page where admins create teacher user accounts.
    DO NOT USE ADMIN SITE'S USER AND TEACHER CREATION PAGES!
    USE THIS FORM INSTEAD TO CREATE TEACHERS!
    Credit to Nipun Brahmbhatt:
    https://blog.botreetechnologies.com/supporting-multiple-roles-using-djangos-user-model-62afa9ce6f61
    :param request:
    :return: teacher registration page and forms.
    """
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


"""

End superuser/admin only views/pages.

"""