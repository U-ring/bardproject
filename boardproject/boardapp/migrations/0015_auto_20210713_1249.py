# Generated by Django 3.2.5 on 2021-07-13 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0014_alter_messages_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='talk_user_id',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='user_id',
            field=models.IntegerField(blank=True),
        ),
    ]
