from django.urls import path
from .views import *

urlpatterns = [
    path('login/', log_in, name='login'),
    path('register/', register, name='register'),
    path('logout/', log_out, name='logout'),
    path('change_password/', change_password),
    path('reset_password/', reset_password),
]
