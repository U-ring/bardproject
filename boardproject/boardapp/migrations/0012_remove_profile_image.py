# Generated by Django 3.2.5 on 2021-07-11 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0011_auto_20210711_0951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]
