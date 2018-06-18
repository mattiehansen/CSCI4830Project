from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pagetwo/', views.pagetwo, name='pagetwo'),
    path('pagethree/', views.pagethree, name='pagethree'),
]