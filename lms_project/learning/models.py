from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission


# Create your models here.
# Verbose_name — удобочитаемое имя поля,
# Default -  Значение по умолчанию для поля
# Свойство blank отвечает за обязательность заполнения поля в админке.
# То есть если указать blank = True - поле будет необязательным к заполнению.
# Если указать blank = False - такое поле обязательно нужно будет заполнить.


class Course(models.Model):
    title = models.CharField(verbose_name='Название курса', max_length=30, unique=True)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, db_table='course_authors', related_name='authors', verbose_name='Автор курса')
    description = models.TextField(verbose_name='Описание курса', max_length=200)
    start_date = models.DateField(verbose_name='Старт курса')
    duration = models.PositiveIntegerField(verbose_name='Продолжительность курса')
    price = models.PositiveIntegerField(verbose_name='Цена', blank=True)
    count_lessons = models.PositiveIntegerField(verbose_name='Кол-во уроков')

    class Meta:
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'
        ordering = ['title']
        permissions = (
            ('modify_course', 'Can modify course content'),
        )

    def __str__(self):
        return f'{self.title}: Cтарт {self.start_date}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'course_id': self.pk})


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='lessons', related_query_name='lesson')
    name = models.CharField(verbose_name='Название урока', max_length=25, unique=True)
    preview = models.TextField(verbose_name='Описание урока', max_length=200)

    class Meta:
        verbose_name_plural = 'Уроки'
        verbose_name = 'Урок'
        ordering = ['course']
        permissions = (
            ('modify_lesson', 'Can modify lesson content'),
        )

    def __str__(self):
        return f'{self.course}: Урок {self.name}'


class Tracking(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, verbose_name='Урок')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Ученик')
    passed = models.BooleanField(default=False, verbose_name='Пройден?')

    class Meta:
        ordering = ['-user']


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Ученик')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    content = models.TextField(verbose_name='Текст отзыва', max_length=250, unique_for_year='sent_date')
    sent_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзывы'
        ordering = ('-sent_date',)
        unique_together = ('user', 'course',)
