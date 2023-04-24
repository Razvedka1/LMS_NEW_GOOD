from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def login(request):
    return HttpResponse('Эта страница для входа пользователя на <b>сайт</b>')


def register(request):
    return HttpResponse('Эта страница для регистрации пользователя')


def logout(request):
    return HttpResponse('Это представление выполняет выход и ридирект на страницу входа')


def change_password(request):
    return HttpResponse('Этот обработчик меняет пароль пользователя')


def reset_password(request):
    return HttpResponse('В этом обработчике реализована логика сброса пароля пользователя')
