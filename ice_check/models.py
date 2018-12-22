from django.db import models
from regions.models import Region
from extended_choices import AutoChoices


# Create your models here.



WATER_TYPE_CHOICES = AutoChoices(
    ('RIVER', 1, 'р.', {'name': 'река'}),
    ('LAKE', 2, 'о.', {'name': 'озеро'}),
    ('RESERVOIR', 3, 'вдх.', {'name': 'водохранилище'}),
    ('POND', 4, 'пруд', {'name': 'пруд'}),
    ('BACKWATER', 5, 'затон', {'name': 'затон'}),
    ('OLDRIVER', 6, 'старица', {'name': 'старица'}),
    ('QUARRY', 7, 'карьер', {'name': 'старица'}),
)


class WaterBody(models.Model):
    name = models.CharField(max_length=50)
    description = models.TestField(max_length=150)

    region = models.ForeignKey(
        Region,
        related_name='water',
        null=True,
        blank=True,
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
        return '{} {}'.format(self.water_type.display, self.name)
