# Generated by Django 3.2 on 2021-05-12 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_file_icon'),
        ('quizzes', '0001_initial'),
        ('core', '0003_topic_quizzes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='articles',
            field=models.ManyToManyField(blank=True, to='core.Article'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='files',
            field=models.ManyToManyField(blank=True, to='files.File'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='quizzes',
            field=models.ManyToManyField(blank=True, to='quizzes.Quiz'),
        ),
    ]
