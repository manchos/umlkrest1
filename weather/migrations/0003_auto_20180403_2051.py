# Generated by Django 2.0.3 on 2018-04-03 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_auto_20180402_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='cloud_score',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0, verbose_name='Облачность (балл)'),
        ),
        migrations.AddField(
            model_name='weather',
            name='is_snow',
            field=models.BooleanField(default=False, verbose_name='Наличие снежного покрова'),
        ),
    ]
