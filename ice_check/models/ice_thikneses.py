from django.db import models
from core.models import TimeStampedModel

from .ice_check_post import IceCheckPost
from crum import get_current_user


class IceThicknessManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()

        if user.is_region:
            return (
                super().get_queryset().filter(
                    ice_check_post__water_body__region_id=user.region_id
                ).select_related('ice_check_post')
                .select_related('ice_check_post__water_body')
            )
        else:
            return (
                super().get_queryset()
                .select_related('ice_check_post__water_body')
                .select_related('water_body')
            )


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

    objects = IceThicknessManager()

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
