# Generated by Django 2.2.6 on 2019-11-25 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20191125_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='showTm',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='watchGrade',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='pubDate',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='movie',
            name='userRating',
            field=models.FloatField(default=0),
        ),
    ]
