from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('change_password/', change_password),
    path('reset_password/', reset_password),
]
