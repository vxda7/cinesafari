# Generated by Django 2.2.6 on 2019-11-22 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20191122_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='link',
        ),
    ]