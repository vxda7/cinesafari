# Generated by Django 2.2.6 on 2019-11-22 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_boxoffice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='userRating',
            field=models.FloatField(),
        ),
    ]