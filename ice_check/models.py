from django.db import models
from regions.models import Region
from extended_choices import AutoChoices
from datetime import datetime
from profiles.models import CustomUser
from core.models import TimeStampedModel
from crum import get_current_user
from django.contrib.gis.db import models as gismodels


# Create your models here.


WATER_TYPE_CHOICES = AutoChoices(
    ('RIVER', 1, 'река', {'name': 'река'}),
    ('LAKE', 2, 'озеро', {'name': 'озеро'}),
    ('RESERVOIR', 3, 'вдх.', {'name': 'водохранилище'}),
    ('POND', 4, 'пруд', {'name': 'пруд'}),
    ('BACKWATER', 5, 'затон', {'name': 'затон'}),
    ('BAY', 6, 'залив', {'name': 'залив'}),
    ('OLDRIVER', 7, 'старица', {'name': 'старица'}),
    ('QUARRY', 8, 'карьер', {'name': 'старица'}),
)


class RegionManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        if user.groups.filter(name='федеральный округ').exists():
            custom_user = CustomUser.objects.get(pk=user.id)
            return super().get_queryset().filter(
                region=custom_user.region
            )
        else:
            return super().get_queryset()


class WaterBody(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250, null=True, blank=True)

    region = models.ForeignKey(
        Region,
        related_name='water_bodies',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Регион",
    )

    water_type = models.PositiveSmallIntegerField(
        choices=WATER_TYPE_CHOICES,
        default=WATER_TYPE_CHOICES.RIVER,
        verbose_name='Тип водоема',
    )

    objects = RegionManager()

    class Meta:
        db_table = 'water_bodies'
        verbose_name = 'Водоемы'
        verbose_name_plural = 'Водоемы'

    def __str__(self):
        return '{} {}'.format(WATER_TYPE_CHOICES.for_value(
            self.water_type).display, self.name)


class PostRegionManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        if user.groups.filter(name='федеральный округ').exists():
            custom_user = CustomUser.objects.get(pk=user.id)
            return super().get_queryset().filter(
                water_body__region=custom_user.region
            )
        else:
            return super().get_queryset()


class IceCheckPost(gismodels.Model):
    name = models.CharField(max_length=100)
    water_body = models.ForeignKey(
        WaterBody,
        related_name='ice_check_posts',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Водоем",
    )

    location = gismodels.PointField(
        srid=4326,
        null=True,
        blank=True,
        verbose_name='Координаты',
    )

    objects = PostRegionManager()

    def __str__(self):
        return '{}, {}'.format(self.water_body, self.name)

    class Meta:
        db_table = 'ice_check_posts'
        verbose_name = 'Пункт измерения льда'
        verbose_name_plural = 'Пункты измерения льда'


class IceThicknessManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        if user.groups.filter(name='федеральный округ').exists():
            custom_user = CustomUser.objects.get(pk=user.id)
            return super().get_queryset().filter(
                ice_check_post__water_body__region=custom_user.region
            )
        else:
            return super().get_queryset()


class IceThickness(TimeStampedModel):
    thick_val_min = models.PositiveSmallIntegerField(
        default=0,
        null=True,
        blank=False,
        verbose_name='Минимальное значение (см)',
    )

    thick_val_max = models.PositiveSmallIntegerField(
        default=0,
        null=True,
        blank=False,
        verbose_name='Максимальное значение (см)',
    )

    thick_val_average = models.PositiveSmallIntegerField(
        default=0,
        null=True,
        blank=False,
        verbose_name='Преобладающее значение (см)',
    )

    check_date = models.DateField(
        null=True,
        blank=False,
        verbose_name='Дата измерения',
    )

    ice_check_post = models.ForeignKey(
        IceCheckPost,
        related_name='ice_thickneses',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Пункт измерения",
    )

    description = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Описание',
        default='',
    )



    def __str__(self):
        return '{}: {}-{} см., преобладает: {} см. {}'.format(
            self.ice_check_post,
            self.thick_val_min,
            self.thick_val_max,
            self.thick_val_average,
            self.description if self.description else '',
        )

    class Meta:
        db_table = 'ice_check_posts_values'
        verbose_name = 'Толщина льда'
        verbose_name_plural = 'Толщина льда'
