from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from .functions import get_timestamp_path_user


# Create your models here.
# Verbose_name — удобочитаемое имя поля,
# Default -  Значение по умолчанию для поля
# Свойство blank отвечает за обязательность заполнения поля в админке. То есть если указать blank = True - поле будет необязательным к заполнению. Если указать blank = False - такое поле обязательно нужно будет заполнить.

class User(AbstractUser):  # Описание в таблице в базе данных
    email = models.EmailField(unique=True, verbose_name='Email')
    birthday = models.DateField(verbose_name='Дата рождения', blank=False)
    description = models.TextField(verbose_name='Обо мне',  max_length=100, null=True, blank=True, default='')
    avatar = models.ImageField(verbose_name='Фото', blank=True, upload_to=get_timestamp_path_user)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = 'Участники'
        verbose_name = 'Участник'
        ordering = ['last_name']

    def __str__(self):
        return f'Участник {self.first_name} {self.last_name}: {self.email}'
