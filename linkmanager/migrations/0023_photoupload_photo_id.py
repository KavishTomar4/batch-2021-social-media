# Generated by Django 4.1.1 on 2022-11-10 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkmanager', '0022_alter_notification_notification_img_src'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoupload',
            name='photo_id',
            field=models.IntegerField(default='0'),
        ),
    ]