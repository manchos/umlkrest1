# Generated by Django 2.1.4 on 2018-12-24 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ice_check', '0008_auto_20181224_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icethickness',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Описание'),
        ),
    ]
