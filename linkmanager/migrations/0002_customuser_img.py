# Generated by Django 4.1.1 on 2022-09-28 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='img',
            field=models.ImageField(default='', upload_to='shop/images'),
        ),
    ]
