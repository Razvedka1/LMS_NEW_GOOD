from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.views.decorators.cache import cache_control, never_cache
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', cache_control(privte=True) (UserLoginView.as_view()), name='login'),
    path('register/', cache_control(privte=True) (RegisterView.as_view()), name='register'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    # Обработчик для смены пароля
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    # Обработчик для сброса пароля
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
#path('logout/', LogoutView.as_view(next_page='login'), log_out, name='logout'),