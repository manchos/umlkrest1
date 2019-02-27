from django.contrib.gis.db import models as gismodels
from django.db import models
from .water_body import WaterBody
from crum import get_current_user


class PostRegionManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        user = get_current_user()
        if user.is_region:
            return (
                super().get_queryset().filter(
                    water_body__region_id=user.region_id
                ).select_related('water_body')
                .select_related('water_body__region')
            )
        else:
            return (
                super().get_queryset()
                .select_related('water_body')
                .select_related('water_body__region')
            )


class IceCheckPost(gismodels.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
    )
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

    def get_region(self):
        return self.water_body.region

    def __str__(self):
        return '{}, {}'.format(self.water_body.name, self.name)

    class Meta:
        db_table = 'ice_check_posts'
        verbose_name = 'Пункт измерения льда'
        verbose_name_plural = 'Пункты измерения льда'