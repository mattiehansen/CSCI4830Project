from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'schoolpass/index.html')


def pagetwo(request):
    return render(request, 'schoolpass/pagetwo.html')


def pagethree(request):
    return render(request, 'schoolpass/pagethree.html')


def rejected(request):
    return render(request, 'schoolpass/rejected.html')

def returned(request):
    return render(request, 'schoolpass/returned.html')