# Generated by Django 3.2.5 on 2021-07-08 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0007_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='//medi/ano.png', upload_to=''),
            preserve_default=False,
        ),
    ]
