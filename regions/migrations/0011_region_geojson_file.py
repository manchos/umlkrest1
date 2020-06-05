# Generated by Django 2.1.4 on 2019-01-11 03:19

from django.db import migrations, models
import regions.models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0010_region_map_center'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='geojson_file',
            field=models.FileField(blank=True, null=True, upload_to=regions.models.region_directory_path),
        ),
    ]