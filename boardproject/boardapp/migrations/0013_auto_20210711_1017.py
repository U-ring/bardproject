# Generated by Django 3.2.5 on 2021-07-11 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0012_remove_profile_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nopes',
            old_name='noped_user_id',
            new_name='liked_user_id',
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='ano.png', upload_to=''),
            preserve_default=False,
        ),
    ]
