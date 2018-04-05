from django.db import models
from weather.dovsoa import get_dovsoa, get_dovsoa_word, get_time_of_day
# from weather.meteo_info import


from django.utils import timezone
# from django.utils import timezone

# Create your models here.


class Weather(models.Model):

    city_name = models.CharField(
        max_length=50,
        default='Moscow',
        verbose_name='Название города',
        editable=False,
    )


    dtime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время',
        editable=False,
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

    wind_speed = models.FloatField(
        blank=False,
        verbose_name='Скорость ветра (м/с)',
        default=0,
    )

    WIND_DIRECTION_CHOICES = (
        ('N', 'северный'),
        ('S', 'южный'),
        ('E', 'восточный'),
        ('W', 'западный'),
        ('NE', 'северо-восточный'),
        ('NW', 'северо-западный'),
        ('SW', 'юго-западный'),
        ('SE', 'юго-восточный'),
    )

    wind_direction = models.CharField(
        max_length=20,
        blank=True,
        choices=WIND_DIRECTION_CHOICES,
        verbose_name='Направление ветра',
        default='NW',
    )

    air_t = models.IntegerField(
        blank=False,
        verbose_name='Температура воздуха (C)',
        default=20,
    )

    # (1 атм = 760 мм рт. ст.)
    atmospheric_pressure = models.IntegerField(
        blank=False,
        verbose_name='Атмосферное давление (мм рт. ст.)',
        default=760,
    )

    is_snow = models.BooleanField(
        blank=True,
        verbose_name='Наличие снежного покрова',
        default=False,
    )

    CLOUD_SCORE_CHOICES = zip(range(0, 11), range(0, 11))

    cloud_score = models.PositiveSmallIntegerField(
        verbose_name='Облачность (балл)',
        choices=CLOUD_SCORE_CHOICES,
        default=0,
        blank=True,
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
        null=True,
        verbose_name='Cтепень вертикальной устойчивости воздуха',
    )

    def get_atmospheric_pressure_in_atm(self):
        return round(self.atmospheric_pressure/760, 4)

    def __str__(self):
        return 'ветер: {} м/с; температура: {} град. С; СВУВ: {}'.format(
            self.wind_speed,
            self.air_t,
            self.get_dovsoa_display(),
        )

    class Meta:
        db_table = 'weather'
        verbose_name = 'Погодные условия'
        verbose_name_plural = 'Погодные условия'



from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver


# @receiver(pre_save, sender=Weather)
# def calc_time_of_day(sender, instance, **kwargs):
#     if not instance.time_of_day:
#         if not instance.crash_dtime:
#             instance.crash_dtime = timezone.now()
#         instance.time_of_day = get_time_of_day(instance.crash_dtime)
#         print('time of day {}'.format(instance.time_of_day))



@receiver(pre_save, sender=Weather)
def calc_dovsoa(sender, instance, **kwargs):
    if instance.time_of_day:
        instance.dovsoa = get_dovsoa(
            time_of_day=instance.time_of_day,
            wind_speed=instance.wind_speed,
            cloudiness=False,
            snow=False,
        )
        print('dovsoa {}'.format(instance.dovsoa))