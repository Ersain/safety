# Generated by Django 3.2 on 2021-05-12 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
