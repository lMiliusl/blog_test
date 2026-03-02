from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets

class User(AbstractUser):
    token = models.CharField(
        max_length=256,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Токен доступа'
    )

    registered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )

    def generate_token(self):
        self.token = secrets.token_urlsafe(192)
        self.save(update_fields=['token'])
        return self.token
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'