# Generated by Django 4.1.1 on 2022-11-08 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkmanager', '0019_notification_notify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(default=''),
        ),
    ]
