# Generated by Django 4.1.1 on 2022-10-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkmanager', '0010_photoupload_user_img_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commenting_user', models.CharField(max_length=122)),
                ('commenting_photo_url', models.CharField(max_length=122)),
                ('comment', models.CharField(max_length=500)),
            ],
        ),
    ]
