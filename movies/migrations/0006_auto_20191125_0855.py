# Generated by Django 2.2.6 on 2019-11-24 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_reveiw'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Boxoffice',
        ),
        migrations.AddField(
            model_name='movie',
            name='boxoffice',
            field=models.IntegerField(default=0),
        ),
    ]
