# Generated by Django 2.1.4 on 2018-12-23 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ice_check', '0003_auto_20181222_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='IceThickness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thick_val_min', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Минимальное значение (см)')),
                ('thick_val_max', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Максимальное значение (см)')),
                ('thick_val_average', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Преобладающее значение (см)')),
                ('description', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ice_thickness', to=settings.AUTH_USER_MODEL)),
                ('ice_check_post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ice_check_posts', to='ice_check.IceCheckPost', verbose_name='Пункт измерения')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Толщина льда',
                'verbose_name_plural': 'Толщина льда',
                'db_table': 'ice_check_posts_values',
            },
        ),
        migrations.AlterField(
            model_name='waterbody',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='water_bodies', to='regions.Region', verbose_name='Регион'),
        ),
        migrations.AlterField(
            model_name='waterbody',
            name='water_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'река'), (2, 'озеро'), (3, 'вдх.'), (4, 'пруд'), (5, 'затон'), (6, 'старица'), (7, 'карьер')], default=1, verbose_name='Тип водоема'),
        ),
    ]