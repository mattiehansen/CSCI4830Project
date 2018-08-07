from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Student, Teacher, Pass


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'last_login',
                    'is_student', 'is_teacher', 'is_staff', 'is_superuser', 'is_active', ]


class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ['__str__', 'user', 'last_logged_in', 'classes', 'accommodations',
                    'notes', 'number_of_passes', 'number_of_rejections', ]


class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ['__str__', 'user', 'last_logged_in', 'classes', 'room_number', ]


class PassAdmin(admin.ModelAdmin):
    model = Pass
    list_display = ['student', 'teacher', 'description', 'id', 'time_left', 'time_returned']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Pass, PassAdmin)
