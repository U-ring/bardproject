# Generated by Django 3.2.5 on 2021-07-16 02:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0019_alter_messages_send_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='send_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
