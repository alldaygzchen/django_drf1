# Generated by Django 4.1.5 on 2023-01-28 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='owner',
        ),
    ]
