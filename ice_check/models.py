from django.db import models
from regions.models import Region
from extended_choices import AutoChoices
from datetime import datetime
from profiles.models import CustomUser


# Create your models here.


WATER_TYPE_CHOICES = AutoChoices(
    ('RIVER', 1, 'река', {'name': 'река'}),
    ('LAKE', 2, 'озеро', {'name': 'озеро'}),
    ('RESERVOIR', 3, 'вдх.', {'name': 'водохранилище'}),
    ('POND', 4, 'пруд', {'name': 'пруд'}),
    ('BACKWATER', 5, 'затон', {'name': 'затон'}),
    ('OLDRIVER', 6, 'старица', {'name': 'старица'}),
    ('QUARRY', 7, 'карьер', {'name': 'старица'}),
)


class RegionManager(models.Manager):
    def get_queryset(self):
        return super()

    # .get_queryset().filter(author='Roald Dahl')



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

    class Meta:
        db_table = 'water_bodies'
        verbose_name = 'Водоемы'
        verbose_name_plural = 'Водоемы'

    def __str__(self):
        return '{} {}'.format(WATER_TYPE_CHOICES.for_value(self.water_type).display, self.name)


class IceCheckPost(models.Model):
    name = models.CharField(max_length=100)
    water_body = models.ForeignKey(
        WaterBody,
        related_name='ice_check_posts',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Водоем",
    )

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = 'ice_check_posts'
        verbose_name = 'Пункт измерения льда'
        verbose_name_plural = 'Пункты измерения льда'


class IceThickness(models.Model):
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

    check_date = models.DateTimeField(null=True, blank=False)

    ice_check_post = models.ForeignKey(
        IceCheckPost,
        related_name='ice_check_posts',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name="Пункт измерения",
    )

    description = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    created_by = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.SET_NULL,
        related_name='ice_thickness',
    )
    updated_by = models.ForeignKey(
        CustomUser,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '{}-{} {} {}'.format(
            self.thick_val_min,
            self.thick_val_max,
            self.thick_val_average,
            self.description,
        )

    class Meta:
        db_table = 'ice_check_posts_values'
        verbose_name = 'Толщина льда'
        verbose_name_plural = 'Толщина льда'
