from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from .views import index
from .models import CustomUser, Student
from .forms import UserForm


class Test(TestCase):

    def test_index(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'schoolpass/index.html', 'schoolpass/base.html')

    def test_uses_login_template(self):
        response = self.client.get('/accounts/login/')
        self.assertTemplateUsed(response, 'registration/login.html', 'schoolpass/base.html')

    def test_custom_user_creation(self, username='testusername', email='example@example.com', password='somepassword'):
        return CustomUser.objects.create(username=username, email=email, password=password)

    def test_student_creation(self, username='testusername', email='example@example.com', password='somepassword',):
        u = CustomUser.objects.create(username=username, email=email, password=password,)
        return Student.objects.create(user=u, classes_enrolled='classes')