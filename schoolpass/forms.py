from django import forms
#from .models import Student, Teacher, Pass
from .models import CustomUser, Student
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'classes', 'is_student',)


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=True,)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'classes', 'is_student',)

class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'classes')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('accommodations', 'notes',)

class LoginForm(forms.Form):
    pass


class PassForm(forms.Form):
    pass


class ReturnForm(forms.Form):
    pass
