# Generated by Django 2.1.4 on 2018-12-18 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0006_auto_20181218_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='slug_name',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Идентификатор'),
        ),
    ]
