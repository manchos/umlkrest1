# Generated by Django 2.0.3 on 2018-04-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd90', '0027_auto_20180402_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rd90calc',
            name='evaporation_duration',
            field=models.DurationField(blank=True, editable=False, verbose_name='Продолжительность испарения вещества'),
        ),
    ]
