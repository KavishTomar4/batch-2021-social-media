# Generated by Django 4.1.1 on 2022-10-01 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkmanager', '0005_alter_customuser_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='img',
        ),
        migrations.AddField(
            model_name='customuser',
            name='img_src',
            field=models.TextField(default=''),
        ),
    ]
