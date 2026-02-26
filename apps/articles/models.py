from django.db import models
from apps.users.models import User

class Category(models.Model):
    name = models.CharField(
    max_length=100,
    unique=True,
    verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

class Article(models.Model):
    title = models.CharField(

        max_length=200,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        verbose_name='Содержание'
    )

    #Связи с пользователем
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name='Категория'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return f'{self.title} (автор: {self.author.username})'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']