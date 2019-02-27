from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.db.models.functions import Centroid, AsGeoJSON
import logging
# Create your models here.
logging.debug('Debug Message')

# from profiles.models import CustomUser

# Create your models here.

from mptt.models import MPTTModel, TreeForeignKey


def region_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.slug_name, filename)


# Check whether actual file of FileField exists (is not deleted / moved out).
def file_exists(obj):
    return obj.storage.exists(obj.name)


class Region(MPTTModel, gismodels.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название',
    )
    short_name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Сокращенное название'
    )
    slug_name = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Идентификатор',
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Входит в',
    )
    borders = gismodels.MultiPolygonField(
        srid=4326,
        null=True,
        blank=True,
        verbose_name='границы региона',
    )

    map_center = gismodels.PointField(
        srid=4326,
        null=True,
        blank=True,
        verbose_name='центр карты',
    )

    geojson_file = models.FileField(
        upload_to=region_directory_path,
        blank=True,
        null=True,
        verbose_name='geojson файл границ региона',
    )

    def save(self, *args, **kwargs):
        if file_exists(self.geojson_file):
            with self.geojson_file.open(mode='r') as file_handler:
                borders = file_handler.read()
                self.borders = borders

        # if self.geojson_file and file_exists(self.geojson_file):
        #     self.geojson_file.open(mode='rb')

        if self.borders:
            regions = Region.objects.annotate(center=Centroid('borders'))
            self.map_center = regions.get(pk=self.pk).center

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регион'
