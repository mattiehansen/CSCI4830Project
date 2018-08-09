from django import forms
from .models import CustomUser, Student, Teacher
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)


class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('classes_enrolled', 'accommodations', 'notes',)


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('classes_taught', 'room_number',)


class PassForm(forms.Form):
    description = forms.CharField(max_length=30)
    teacher_username = forms.CharField(max_length=150)
    teacher_password = forms.CharField(widget=forms.PasswordInput)


class ReturnForm(forms.Form):
    teacher_username = forms.CharField(max_length=150)
    teacher_password = forms.CharField(widget=forms.PasswordInput)
