# Generated by Django 2.2.6 on 2019-11-25 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20191125_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
