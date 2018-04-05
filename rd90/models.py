from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone

from weather.dovsoa import get_time_of_day

# from hazard_substance.models import HazardousChemical

from geobjects.models import Object, SubstanceAmount
from weather.models import Weather
import rd90.calculation as calc
from django.contrib.postgres.fields import JSONField



class Rd90Calc(models.Model):

    crash_dtime = models.DateTimeField(
        null=True,
        blank=True,
        # auto_now_add=True,
        verbose_name='Время аварии',
    )

    after_crash_time = models.DurationField(
        null=True,
        blank=True,
        verbose_name='Количество минут после аварии',
        default=timedelta(hours=1),
    )

    # weather = models.ForeignKey(
    #     Weather,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     verbose_name='Погодные условия',
    # )

    weather = models.ForeignKey(
        Weather,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Погодные условия',
    )


    # chemical = models.ForeignKey(
    #     HazardousChemical,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     verbose_name='АХОВ',
    # )

    chem_danger_object = models.ForeignKey(
        Object,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='ХОО',
    )

    chemical = models.ForeignKey(
        SubstanceAmount,
        blank=True,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Количество вещества (т)',
    )
    chemical.short_description = "Выберете для какого вещества на объекте производится расчет"




    # FULL = 'full'
    # ONE_TANK = 'one_tank'
    # IS_SET = 'is_set'
    #
    #
    # AMOUNT_FOR_CHOICES = (
    #     (FULL, 'всех емкостей'),
    #     (ONE_TANK, 'одной емкости'),
    # )
    #
    #
    #
    # chemicals_amount_calc = models.CharField(
    #     max_length=10,
    #     choices=AMOUNT_FOR_CHOICES,
    #     default=FULL,
    #     verbose_name='Расчет для:',
    # )


    # chemicals_amount = models.IntegerField(
    #     blank=True,
    #     verbose_name='Количество вещества',
    #     default=0,
    # )
    # chemicals_amount.short_description = "Будет задано исходя из поля Расчет для"

    #
    # STORAGE_CHOICES = (
    #     ('liquid', 'жидкость'),
    #     ('gas', 'газ'),
    #     ('calc', 'вычисляется')
    # )
    #
    # hc_storage = models.CharField(
    #     max_length=8,
    #     choices=STORAGE_CHOICES,
    #     default='calc',
    #     verbose_name='Способ хранение АХОВ',
    # )

    # # K4 - коэффициент, учитывающий скорость ветра
    # k4 = models.FloatField(
    #     blank=True,
    #     default=0,
    #     verbose_name='K4 - коэффициент',
    #     editable=False,
    # )
    #
    # # K5 - коэффициент, учитывающий степень вертикальной устойчивости атмосферы
    # k5 = models.FloatField(
    #     blank=True,
    #     default=0,
    #     verbose_name='K5 - коэффициент',
    #     editable=False,
    # )
    # # K6 - коэффициент, зависящий от времени N, прошедшего после начала аварии;
    # k6 = models.FloatField(
    #     blank=True,
    #     default=0,
    #     verbose_name='K5 - коэффициент',
    #     editable=False,
    # )

    evaporation_duration = models.DurationField(
        blank=True,
        null=True,
        verbose_name='Продолжительность испарения вещества',
        editable=False,
    )

    full_contamination_depth = models.FloatField(
        blank=True,
        verbose_name='Полная глубина зоны заражения Г (км)',
        default=0,
        max_length=500.0,
        editable=False,
    )

    angular_size = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name='Значение углового размера зоны заражения (град)',
        default=0,
        editable=False,
    )

    possible_contamination_area = models.FloatField(
        blank=True,
        verbose_name='Площадь зоны возможного заражения АХОВ (квадр. км)',
        default=0,
        editable=False,
    )

    actual_contamination_area = models.FloatField(
        blank=True,
        verbose_name='Площадь зоны фактического заражения АХОВ (квадр. км)',
        default=0,
        editable=False,
    )

    json_calculation = JSONField()

    # def save(self, *args, **kwargs):
    #
    #
    #
    #     super(Rd90Calc, self).save(*args, **kwargs)




    def __str__(self):
        return 'АХОВ: {}; Погода: {}'.format(self.chemical, self.weather)

    class Meta:
        db_table = 'rd90calcs'
        verbose_name = 'РД 90 расчет'
        verbose_name_plural = 'РД 90 расчеты'


from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver


# @receiver(post_init, sender=Rd90Calc)
# def set_default_datetime(sender, instance, **kwargs):
#     if not instance.crash_dtime:
#         print('dddddddddddddddddddddd')
#         instance.crash_dtime = now()


@receiver(pre_save, sender=Rd90Calc)
def calc_time_of_day(sender, instance, **kwargs):
    # if not instance.weather.time_of_day:
    if instance.crash_dtime:
        # instance.crash_dtime = timezone.now()
        instance.weather.time_of_day = get_time_of_day(instance.crash_dtime)
        instance.weather.save()

        print('time of day {}'.format(instance.weather.time_of_day))


@receiver(pre_save, sender=Rd90Calc)
def calc_rd90(sender, instance, **kwargs):
    rd90 = calc.RD90(instance)
    instance.evaporation_duration = rd90.evaporation_duration
    instance.full_contamination_depth = rd90.full_contamination_depth
    instance.angular_size = rd90.angular_size
    instance.possible_contamination_area = rd90.possible_contamination_area
    instance.actual_contamination_area = rd90.actual_contamination_area
    instance.json_calculation = rd90.json
    print('evaporation_duration %s' % instance.evaporation_duration)


    # danger_object = instance.chem_danger_object
    # if instance.chemicals_amount_calc == instance.st.FULL:
    #     pass
    #     # danger_object.su
    #     # instance.chemicals_amount = instance.chemical.get()
    #     # SubstanceAmount.objects.select_related('blog').get(id=5)
    #     pass
    #     # if
    # else:
    #     SubstanceAmount.objects.get(object=instance.chemical, amount_for='one_tank')

    # OO.substanceamount_set.get(amount_for='full')





    # if instance.chemicals_amount_calc == 'tank_substance_amount':
        #     instance.chemicals_amount = instance.chemical.tank_substance_amount
        # SubstanceAmount.objects.filter(object__name=instance.chem_danger_object)
        # print(instance.chem_danger_object)
        # instance.chemicals_amount = instance.chem_danger_object.substance_amounts


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