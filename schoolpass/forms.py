from django import forms
from .models import Student, Teacher, Pass

class LoginForm(forms.Form):
    pass
    #student_id = forms.IntegerField(min_value=1000000000, max_value=9999999999)
    #password = forms.CharField(widget=forms.PasswordInput)


class PassForm(forms.Form):
    pass


class ReturnForm(forms.Form):
    pass
