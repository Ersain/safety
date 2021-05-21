from django.conf import settings
from django.db import models


class Notification(models.Model):
    title = models.CharField(
        default='Поздравляем!',
        max_length=100
    )
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.pk} {self.title} - {self.user}'


class Achievement(models.Model):
    title = models.CharField(
        default='Поздравляем!',
        max_length=100
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.body}'
