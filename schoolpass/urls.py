from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pagetwo/', views.pagetwo, name='pagetwo'),
    path('pagethree/', views.pagethree, name='pagethree'),
    path('rejected/', views.rejected, name='rejected'),
    path('returned/', views.returned, name='returned'),
    path('registration_forms/', views.registration_forms, name='registration_forms'),
    path('student_registration/', views.student_registration, name='student_registration'),
    path('teacher_registration/', views.teacher_registration, name='teacher_registration'),
    path('process_pass/', views.process_pass, name='process_pass'),
]
