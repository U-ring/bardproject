# Generated by Django 3.2.5 on 2021-07-15 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0016_remove_messages_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='send_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]