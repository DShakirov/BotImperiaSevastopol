from django.db import models
from typing import Dict

from bot import utils


class Category(models.Model):

    title = models.CharField(max_length=150, verbose_name='Категория')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


#то, что мы отправляем пользователю
class Post(models.Model):

    title = models.CharField(max_length=150, verbose_name='Пост')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='Контент')
    image = models.ImageField(verbose_name='Изображение',upload_to='images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    on_top = models.BooleanField(default=False, verbose_name='Закрепленная запись')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['on_top','-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True, verbose_name='Логин')
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, null=True, blank=True, verbose_name='Фамилия')
    language_code = models.CharField(max_length=8, null=True, blank=True, verbose_name="Язык клиента")
    deep_link = models.CharField(max_length=64, null=True, blank=True)
    is_blocked_bot = models.BooleanField(default=False, verbose_name='Заблокирован')
    is_banned = models.BooleanField(default=False, verbose_name='Забанен')
    is_admin = models.BooleanField(default=False, verbose_name='Админ')
    is_moderator = models.BooleanField(default=False, verbose_name='Модератор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def get_user_and_created(cls, update, context):
        data = utils.extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)

        if created:
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update, context):
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, string):
        """ Search user in DB, return User or None if not found """
        username = str(string).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    def invited_users(self):  # --> User queryset
        return User.objects.filter(deep_link=str(self.user_id), created_at__gt=self.created_at)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserActionLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=128, verbose_name='Действие')
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата, время активности')

    def __str__(self):
        return f"user: {self.user}, made: {self.action}, created at {self.created_at.strftime('(%H:%M, %d %B %Y)')}"

    class Meta:
        verbose_name = 'Действия пользователей'
        verbose_name_plural = 'Действия пользователей'


#то, что мы получаем от пользователя
class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(blank=True, null=True, verbose_name='Текст')
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата, время сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

