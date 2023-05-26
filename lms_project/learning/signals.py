from django.db.models.signals import pre_save
from .models import Course, Lesson


def check_quantity(sender, instance, **kwargs):
    error = None
    actual_count = sender.objects.filter(course=instance.course).count()
    set_count = Course.objects.filter(id=instance.course.id).values('count_lessons')[1]['count_lessons']

    if actual_count >= set_count:
        error = f'Колличество уроков ограничено' \
                f'Ранее вы установили, что курс будет содержать {set_count} уроков'

    return error


pre_save.connect(check_quantity, sender=Lesson)