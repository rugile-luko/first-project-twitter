# Generated by Django 2.2.7 on 2019-11-19 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_remove_comment_users_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='comment',
        ),
    ]
