from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import  LoginForm, RegisterForm
from .models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

# Create your views here.

class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    next_page = 'index'

class RegisterView(CreateView):
    form_class = 'register.html'

    def form_valid(self, form):
        user = form.save('')
        pupil = Group.objects.filter(name='Ученик')
        user.groups.set(pupil)
        login(self.request, user)
        return redirect('index')
1. Метод `form_valid` принимает два аргумента: `self` (который относится к текущему экземпляру класса) и `form` (который является проверенными данными формы).

2. Метод form.save() сохраняет данные формы в базу данных и возвращает пользовательский объект.

3. Переменная «ученик» запрашивает модель «Группа», чтобы получить групповой объект с именем «Студент».

4. Метод user.groups.set(pupil) добавляет пользователя в группу «Студент».

5. Функция входа в систему позволяет пользователю войти в систему.

6. Оператор return redirect('index')` перенаправляет пользователя на индексную страницу веб-сайта.















#
#def log_in(request):
#    if request.method == 'POST':
#        data = request.POST
#        user = authenticate(email=data['email'], password=data['password'])
#        if user and user.is_active:
#            login(request, user)
#            return redirect('index')
#        else:
#            return HttpResponse('Ваш аккаунт заблокирован')
#    else:
#        return render(request, 'login.html')
#

#def register(request):
#    if request.method == 'POST':
#        data = request.POST
#        new_user = User(email=data['email'], first_name=data['first_name'], last_name=data['last_name'],
#                    birthday=data['birthday'], description=data['description'], avatar=data['avatar'])
#        new_user.set_password(data['password'])
#        new_user.save()
#        pupil = Group.objects.filter(name='Ученик')
#        new_user.groups.set(pupil)
#        login(request, new_user)
#        return redirect('index')
#    else:
#        return render(request, 'register.html')


#def log_out(request):
#    logout(request)
#    return redirect('login')


#def change_password(request):
#    return HttpResponse('Этот обработчик меняет пароль пользователя')


#def reset_password(request):
#    return HttpResponse('В этом обработчике реализована логика сброса пароля пользователя')
