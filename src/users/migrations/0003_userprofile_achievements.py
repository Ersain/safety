# Generated by Django 3.2.3 on 2021-05-20 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
        ('users', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='achievements',
            field=models.ManyToManyField(blank=True, to='notifications.Achievement'),
        ),
    ]
