# Generated by Django 2.0.3 on 2018-03-29 11:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rd90', '0014_auto_20180329_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rd90calc',
            name='crash_dtime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 3, 29, 11, 46, 46, 794617, tzinfo=utc), null=True, verbose_name='Время аварии'),
        ),
    ]
