from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import  LoginForm, RegisterForm
from .models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from datetime import datetime
from django.conf import settings

# Create your views here.

class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    next_page = 'courses'

    def form_valid(self, form):
        is_remember = self.request.POST.get('is_remember')
        if is_remember == 'on':
            self.request.session[settings.REMEMBER_KEY] = datetime.now().isoformat()
            self.request.session.set_expiry(settings.REMEMBER_AGE)
        elif is_remember == 'off':
            self.request.session.set_expiry(0)
        return super(UserLoginView, self).form_valid(form)
    

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save()
        pupil = Group.objects.filter(name='Ученик')
        user.groups.set(pupil)
        login(self.request, user)
        return redirect('index')

















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
