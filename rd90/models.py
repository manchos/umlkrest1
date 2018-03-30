from django.db import models
from .utils import get_dovsoa, get_time_of_day, get_dovsoa_word
from datetime import datetime
from django.utils.timezone import now
from hazard_substance.models import HazardousChemical

from geobjects.models import Object

# Create your models here.

# class HazardousChemical(models.Model):
#     name = models.CharField(max_length=255)
#     form = models.CharField(null=True,max_length=255)
#     gas_density = models.FloatField(null=True, blank=True)
#     liquid_density = models.FloatField(null=True, blank=True)
#     boiling_t = models.FloatField(null=True, blank=True)
#     toxodeth = models.FloatField(null=True, blank=True)
#     k1 = models.FloatField(null=True, blank=True)
#     k2 = models.FloatField(null=True, blank=True)
#     k3 = models.FloatField(null=True, blank=True)
#     k7_1 = models.CharField(max_length=255, null=True, blank=True)
#     k7_1_f = models.CharField(max_length=255, null=True, blank=True)
#     k7_2 = models.CharField(max_length=255, null=True, blank=True)
#     k7_2_f = models.CharField(max_length=255, null=True, blank=True)
#     # descr = models.TextField(null=True, blank=True)
#
#     class Meta:
#         db_table = 'HazardousChemicals'
#         verbose_name = 'Коэффициеты'
#         verbose_name_plural = 'Коэффициеты'
#
#     def __str__(self):
#         return '{} {}'.format(self.name, self.form)


class Rd90Calc(models.Model):
    city_name = models.CharField(
        max_length=50,
        default='Moscow',
        verbose_name='Название города'
    )

    TIMEOFDAY_CHOICES = (
        ('morning', 'утро'),
        ('day', 'день'),
        ('evening', 'вечер'),
        ('night', 'ночь'),
        ('', 'вычисляется')
    )

    time_of_day = models.CharField(
        max_length=50,
        blank=True,
        choices=TIMEOFDAY_CHOICES,
        verbose_name='Время суток',
        default='',
    )

    crash_dtime = models.DateTimeField(
        null=True,
        blank=True,
        default=now(),
        verbose_name='Время аварии'
    )

    minutes_after_crach = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Количество минут после аварии'
    )

    wind_speed = models.IntegerField(blank=False, verbose_name='Скорость ветра (м/с)')
    air_t = models.IntegerField(blank=False, verbose_name='Температура воздуха (C)')
    chemicals_amount = models.IntegerField(
        blank=True,
        verbose_name='Количество вещества (т)',
        default=0,
    )

    DOVSOA_CHOICES = (
        ('из', 'изотермия'),
        ('ин', 'инверсия'),
        ('к', 'конверсия'),
        ('', 'вычисляется'),
    )

    dovsoa = models.CharField(
        max_length=10,
        blank=True,
        choices=DOVSOA_CHOICES,
        default='',
        verbose_name='Cтепень вертикальной устойчивости воздуха',
    )

    chemical = models.ForeignKey(
        HazardousChemical,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='АХОВ',
    )
    chem_danger_object = models.ForeignKey(
        Object,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='ХОО',
    )

    STORAGE_CHOICES = (
        ('liquid', 'жидкость'),
        ('gas', 'газ'),
    )

    hc_storage = models.CharField(
        max_length=8,
        choices=STORAGE_CHOICES,
        default='gas',
        verbose_name='Хранение АХОВ',
    )

    def __str__(self):
        return 'ХОО: {} АХОВ: {}; ветер: {} м/с; температура: {} град. С; СВУВ: {}'.format(
            self.chem_danger_object, self.chemical, self.wind_speed, self.air_t, get_dovsoa_word(self.dovsoa))

    class Meta:
        db_table = 'rd90calcs'
        verbose_name = 'РД 90 расчет'
        verbose_name_plural = 'РД 90 расчеты'


from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Rd90Calc)
def calc_time_of_day(sender, instance, **kwargs):
    if not instance.time_of_day:
        instance.time_of_day = get_time_of_day(instance.crash_dtime)

@receiver(pre_save, sender=Rd90Calc)
def calc_dovsoa(sender, instance, **kwargs):
    if not instance.dovsoa:
        instance.dovsoa = get_dovsoa(
            time_of_day=instance.time_of_day,
            wind_speed=instance.wind_speed,
            cloudiness=False,
            snow=False,
        )


@receiver(pre_save, sender=Rd90Calc)
def calc_dovsoa(sender, instance, **kwargs):
    if not instance.dovsoa:
        instance.dovsoa = get_dovsoa(
            time_of_day=instance.time_of_day,
            wind_speed=instance.wind_speed,
            cloudiness=False,
            snow=False,
        )

#
# time_of_day = get_time_of_day(crash_dtime)  # время дня
# air_t = 20  # температура воздуха
# q = 12  # количество выброшенного (разлившегося) при аварии вещества, т
# wind_speed = 2  # скорость ветра
# time_of_day = 'night'
# dovsoa = 'из'
#
# if crash_dtime:
#     time_of_day = get_time_of_day(crash_dtime, city_name)
#     estimated_dtime = datetime(2017, 4, 19, 3, 30)
#     after_crash_time = estimated_dtime - crash_dtime  # время после аварии
#
# if not dovsoa:
#     dovsoa = get_dovsoa(time_of_day, wind_speed)
# hcs_id = 30  # id вещества  хлор = 30
# hcs_storage = 'liquid'  # условия хранения АХОВ
#
# hours, minutes = 1, 0  # количество часов и минут после аварии