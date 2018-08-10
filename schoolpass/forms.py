from django import forms
from .models import CustomUser, Student, Teacher
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a CustomUser
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):
    """
    Form for editing a CustomUser
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',)


class UserForm(UserCreationForm):
    """
    Form that is used as a part of creating a student or teacher account.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class StudentForm(forms.ModelForm):
    """
    Form used along UserForm to create a student account.
    NEVER MARK STUDENTS AS STAFF OR SUPERUSERS ON ADMIN SITE!
    """
    class Meta:
        model = Student
        fields = ('classes_enrolled', 'accommodations', 'notes',)


class TeacherForm(forms.ModelForm):
    """
    Form used along UserForm to create a teacher account.
    Teachers should at least be marked as staff for them to handle passes on admin site after creation.
    """
    class Meta:
        model = Teacher
        fields = ('classes_taught', 'room_number',)


class PassForm(forms.Form):
    """
    Used on pagetwo (AKA accept/reject screen).
    Students can  fill in description of their destination and show to a teacher.
    Teacher then can accept or reject it after putting in their username and password.
    """
    description = forms.CharField(max_length=30)
    teacher_username = forms.CharField(max_length=150)
    teacher_password = forms.CharField(widget=forms.PasswordInput)


class ReturnForm(forms.Form):
    """
    Used on pagethree (AKA pass screen).
    Students can complete their pass when they're on this screen.
    Teacher can then enter their credentials again once they've returned.
    """
    teacher_username = forms.CharField(max_length=150)
    teacher_password = forms.CharField(widget=forms.PasswordInput)
