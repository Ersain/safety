from django.db import models

from .utils import generate_random_url


class FileChoices(models.TextChoices):
    COMIC = ('COMIC', 'Comic')
    VIDEO = ('VIDEO', 'Video')


class File(models.Model):
    code = models.CharField(
        max_length=255,
        unique=True,
        default=generate_random_url,
        db_index=True
    )
    title = models.CharField(
        max_length=100,
        null=True, blank=True
    )
    type = models.CharField(
        max_length=100,
        choices=FileChoices.choices,
        default=FileChoices.VIDEO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    def __str__(self):
        return f'{self.code} [{self.title} - {self.file.name}]'
