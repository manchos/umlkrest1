# Generated by Django 2.0.3 on 2018-04-02 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rd90', '0028_auto_20180402_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rd90calc',
            name='weather',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='weather.Weather', verbose_name='Погодные условия'),
        ),
    ]
