# Generated by Django 3.2.5 on 2021-07-15 09:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0018_alter_messages_send_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='send_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]