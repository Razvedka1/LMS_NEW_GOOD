from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', MainView.as_view(template_name='index.html', queryset=Course.objects.all(), context_object_name='courses'),
         name='index'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='detail'),
    path('create/', CourseCreateView.as_view(), name='create'),  # Параметр name позволяет принимать обратный поиск адресов.
    path('delete/<int:course_id>/', CourseDeleteView.as_view(), name='delete'),
    path('update/<int:course_id>/', CourseUpdateView.as_view(), name='update'),
    path('enroll/<int:course_id>/', enroll, name='enroll'),
    path('review/<int:course_id>/', review, name='review'),
    path('<int:course_id>/create_lesson/', LessonCreateView.as_view(), name='create_lesson')
]
# Рабочий вариант! r'^detail/(?P<course_id>\d+)/$ - бесконечный хоть до 100.
# Рабочий вариант! r'^detail/(?P<course_id>[1-9])/$ - как в  методичке.
