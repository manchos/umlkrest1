# Generated by Django 2.0.3 on 2018-04-03 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geobjects', '0017_auto_20180403_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='substanceamount',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geobjects.Object'),
        ),
    ]
