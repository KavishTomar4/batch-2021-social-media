# Generated by Django 4.1.1 on 2022-10-19 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linkmanager', '0016_alter_comments_comment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_user', models.CharField(max_length=122)),
                ('notification', models.CharField(max_length=122)),
                ('by_user', models.CharField(max_length=122)),
                ('notification_img_src', models.CharField(max_length=122)),
            ],
        ),
    ]