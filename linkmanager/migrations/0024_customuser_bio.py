# Generated by Django 4.1.1 on 2022-11-10 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkmanager', '0023_photoupload_photo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(default=''),
        ),
    ]
