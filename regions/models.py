from django.db import models
from django.contrib.gis.db import models as gismodels

# from profiles.models import CustomUser

# Create your models here.

from mptt.models import MPTTModel, TreeForeignKey


class Region(MPTTModel, gismodels.Model):
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=150, unique=True, )
    slug_name = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Идентификатор',
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    borders = gismodels.MultiPolygonField(
        srid=4326,
        null=True,
        blank=True
    )

    def __str__(self):

        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регион'
