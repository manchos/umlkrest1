# Generated by Django 2.0.3 on 2018-03-29 09:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rd90', '0013_auto_20180329_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rd90calc',
            name='chemicals_amount',
            field=models.IntegerField(blank=True, default=0, verbose_name='Количество вещества (т)'),
        ),
        migrations.AlterField(
            model_name='rd90calc',
            name='crash_dtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 3, 29, 9, 29, 7, 908089, tzinfo=utc), null=True, verbose_name='Время аварии'),
        ),
        # migrations.DeleteModel(
        #     name='HazardousChemical',
        # ),
    ]
