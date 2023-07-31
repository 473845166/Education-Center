from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'app1/base2.html')


def user(request):
    return render(request, 'app1/user.html')


def center(request):
    return render(request, 'app1/center.html')
