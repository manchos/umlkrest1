from django.db import models
from regions.models import Region
from extended_choices import AutoChoices


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
        return '{} {}'.format(WATER_TYPE_CHOICES.for_value(
            self.water_type).display, self.name)
