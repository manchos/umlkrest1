# Generated by Django 2.0.3 on 2018-03-31 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rd90', '0023_rd90calc_wind_direction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rd90calc',
            name='hc_storage',
        ),
    ]
