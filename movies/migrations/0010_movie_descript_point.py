# Generated by Django 2.2.6 on 2019-11-25 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_movie_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='descript_point',
            field=models.TextField(default=''),
        ),
    ]
