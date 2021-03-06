# Generated by Django 3.2.5 on 2021-07-12 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0010_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nopes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('noped_user_id', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='image2',
            field=models.ImageField(default='noPhoto.png', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='image3',
            field=models.ImageField(default='noPhoto.png', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='image4',
            field=models.ImageField(default='noPhoto.png', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='image5',
            field=models.ImageField(default='noPhoto.png', upload_to=''),
            preserve_default=False,
        ),
    ]
