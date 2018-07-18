from django.shortcuts import render
from .models import Student, Teacher, Pass
from .forms import LoginForm, PassForm, ReturnForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST

def index(request):
    student_list = Student.objects.all()
    teacher_list = Teacher.objects.all()
    form = LoginForm
    context = {'teachers': teacher_list, 'students': student_list, 'form': form, }
    return render(request, 'schoolpass/index.html', context)


# @require_POST
def pagetwo(request):
    student_list = Student.objects.all()
    teacher_list = Teacher.objects.all()
    form = PassForm
    context = {'teachers': teacher_list, 'students': student_list, 'form': form, }
    return render(request, 'schoolpass/pagetwo.html', context)


# @require_POST
def pagethree(request):
    student_list = Student.objects.all()
    teacher_list = Teacher.objects.all()
    form = ReturnForm
    context = {'teachers': teacher_list, 'students': student_list, 'form': form, }
    return render(request, 'schoolpass/pagethree.html', context)


# @require_POST
def rejected(request):
    return render(request, 'schoolpass/rejected.html')


# @require_POST
def returned(request):
    return render(request, 'schoolpass/returned.html')