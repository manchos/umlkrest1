# Generated by Django 2.1.4 on 2018-12-22 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ice_check', '0002_auto_20181222_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterbody',
            name='description',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]