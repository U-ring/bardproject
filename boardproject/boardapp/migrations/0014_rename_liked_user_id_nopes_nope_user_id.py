# Generated by Django 3.2.5 on 2021-07-11 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0013_auto_20210711_1017'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nopes',
            old_name='liked_user_id',
            new_name='nope_user_id',
        ),
    ]
