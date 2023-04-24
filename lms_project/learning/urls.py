from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),  # Параметр name позволяет принимать обратный поиск адресов.
    path('delete/<int:course_id>/', delete, name='delete'),
    re_path(r'^detail/(?P<course_id>[1-9])/$', detail, name='detail'),
    path('enroll/<int:course_id>/', enroll, name='enroll'),
]
# Рабочий вариант! r'^detail/(?P<course_id>\d+)/$ - бесконечный хоть до 100.
# Рабочий вариант! r'^detail/(?P<course_id>[1-9])/$ - как в  методичке.
