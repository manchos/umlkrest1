# Generated by Django 2.0.3 on 2018-04-02 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd90', '0029_auto_20180402_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rd90calc',
            name='chemicals_amount_calc',
            field=models.CharField(choices=[('full', 'всех емкостей'), ('one_tank', 'одной емкости'), ('is_set', 'is_set')], default='full', max_length=30, verbose_name='Расчет для:'),
        ),
    ]
