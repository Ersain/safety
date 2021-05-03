from django.db import models

from files.utils import generate_random_url


class Topic(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    code = models.CharField(
        max_length=255,
        default=generate_random_url,
        unique=True,
        db_index=True
    )

    files = models.ManyToManyField(to='files.File')
    articles = models.ManyToManyField(to='core.Article')

    def __str__(self):
        return f'{self.pk} - {self.title}'


class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    code = models.CharField(
        max_length=255,
        default=generate_random_url,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return f'{self.pk} - {self.title}'
