# Generated by Django 2.1.4 on 2018-12-22 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ice_check', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IceCheckPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Пункт измерения льда',
                'verbose_name_plural': 'Пункты измерения льда',
                'db_table': 'ice_check_posts',
            },
        ),
        migrations.AlterField(
            model_name='waterbody',
            name='description',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='waterbody',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='waterbody',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='water_bodies', to='regions.Region', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='icecheckpost',
            name='water_body',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ice_check_posts', to='ice_check.WaterBody', verbose_name='Водоем'),
        ),
    ]
