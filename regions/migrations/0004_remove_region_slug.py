# Generated by Django 2.1.4 on 2018-12-17 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0003_auto_20181218_0017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='region',
            name='slug',
        ),
    ]
