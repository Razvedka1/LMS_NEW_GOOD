from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', log_in, name='login'),
    path('register/', register, name='register'),
    path('logout/', log_out, name='logout'),
    path('change_password/', change_password, name='change_password'),
    # Обработчик для сброса пароля
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
#path('logout/', LogoutView.as_view(next_page='login'), log_out, name='logout'),