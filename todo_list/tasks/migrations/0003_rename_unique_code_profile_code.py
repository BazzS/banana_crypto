# Generated by Django 4.2.2 on 2023-06-19 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='unique_code',
            new_name='code',
        ),
    ]
