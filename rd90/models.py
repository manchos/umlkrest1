from datetime import timedelta

from django.contrib.postgres.fields import JSONField
from django.db import models

import rd90.calc.all as calc
from geobjects.models import Object, SubstanceInfo
from weather.dovsoa import get_time_of_day
from weather.models import Weather



# from django.core import serializers



class Rd90Calc(models.Model):

    owner = models.ForeignKey(
        'auth.User',
        related_name='rd90calcs',
        on_delete=models.CASCADE,
        default=1
    )


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

    chemical = models.ManyToManyField(
        SubstanceInfo,
        verbose_name='Количество вещества',
    )
    chemical.short_description = "Выберете для какого вещества на объекте производится расчет"

    def get_chemicals(self):
        return "\n".join([str(chem) for chem in self.chemical.all()])

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

    json_calculation = JSONField(
        null=True, editable=False
    )


    # def save(self, *args, **kwargs):
    #     chemical_amount = self.chemical.count()
    #     if chemical_amount == 1:
    #         rd90 = calc.RD90(self, self.chemical.first())
    #         self.evaporation_duration = rd90.evaporation_duration
    #         self.full_contamination_depth = rd90.full_contamination_depth
    #         self.angular_size = rd90.angular_size
    #         self.possible_contamination_area = rd90.possible_contamination_area
    #         self.actual_contamination_area = rd90.actual_contamination_area
    #         self.json_calculation = rd90.json
    #         print('evaporation_duration %s' % self.evaporation_duration)
    #
    #     if chemical_amount > 1:
    #
    #         rd90_list = []
    #         after_crash_hours = self.after_crash_time.seconds / 3600
    #
    #         print('self.chemical: %s' % self.chemical)
    #
    #         for chemical in self.chemical.iterator():
    #             rd90_list.append(calc.RD90(self, chemical))
    #
    #         self.evaporation_duration = max(
    #             [rd90.evaporation_duration for rd90 in rd90_list]
    #         )
    #
    #         equivalent_amount = calc.RD90.get_full_equivalent_amount(
    #             wind_speed=self.weather.wind_speed,
    #             dovsoa=self.weather.dovsoa,
    #             rd90_list=rd90_list,
    #         )
    #         contamination_depth = calc.RD90.get_contamination_depth(
    #             equivalent_amount=equivalent_amount,
    #             wind_speed=self.weather.wind_speed,
    #         )
    #         front_speed = calc.RD90.get_front_speed(
    #             wind_speed=self.weather.wind_speed,
    #             dovsoa=self.weather.dovsoa,
    #         )
    #         possible_contamination_depth = calc.RD90.get_possible_contamination_depth(
    #             front_speed=front_speed,
    #             after_crash_time=after_crash_hours,
    #         )
    #         self.full_contamination_depth = min(contamination_depth, possible_contamination_depth)
    #         self.angular_size = calc.RD90.get_angular_size(wind_speed=self.weather.wind_speed)
    #         self.possible_contamination_area = calc.RD90.get_possible_contamination_area(
    #             contamination_depth=contamination_depth,
    #             angular_size=self.angular_size,
    #         )
    #         self.actual_contamination_area = calc.RD90.get_actual_contamination_area(
    #             contamination_depth=contamination_depth,
    #             dovsoa=self.weather.dovsoa,
    #             after_crash_time=after_crash_hours,
    #         )
    #         print('self %s ' % self.__dict__)
    #
    #         # instance_json = serializers.serialize("json", instance)
    #
    #         # instance.json_calculation = ''
    #         instance_dict = self.__dict__
    #
    #         d = dict((k, v) for k, v in instance_dict.items()
    #                  if k not in ['_state', 'json_calculation', 'chemical', 'evaporation_duration', 'k1237',
    #                               'after_crash_time'])
    #         print(d)
    #         self.json_calculation = json.dumps(d, indent=4, sort_keys=True, ensure_ascii=False)
    #         # instance.json_calculation = instance_json
    #
    #
    #
    #         super(Rd90Calc, self).save(*args, **kwargs)




    def __str__(self):
        chems = ''
        for chem in self.chemical.iterator():
            chems += chem.__str__() + ', '
        return 'АХОВ: {}; Погода: {}'.format(chems, self.weather)

    class Meta:
        db_table = 'rd90calcs'
        verbose_name = 'РД 90 расчет'
        verbose_name_plural = 'РД 90 расчеты'


from django.db.models.signals import pre_save, m2m_changed
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


# def handle_flow(sender, instance, *args, **kwargs):

@receiver(m2m_changed, sender=Rd90Calc.chemical.through) #pre_save, sender=Rd90Calc)
def calc_rd90(sender, instance, **kwargs):
    print("+++++++++++++++++++++++++++++++++++++Signal catched !")
    chemical_amount = instance.chemical.count()
    print('chemical_amount: %s' % chemical_amount)

    if chemical_amount == 1:
        # rd90 = calc.RD90(instance, instance.chemical.first())
        chem = instance.chemical.first()
        print('chemical: %s' % chem)
        rd90 = ''
        rd90 = calc.RD90(
            hazard_substance_obj=chem.hazard_substance,
            substance_amount=chem.substance_amount,
            embank_height=chem.embank_height,
            storage_condition=chem.embank_height,
            weather_dovsoa=instance.weather.dovsoa,
            weather_wind_speed=instance.weather.wind_speed,
            weather_air_t=instance.weather.air_t,
            weather_atmospheric_pressure=instance.weather.get_atmospheric_pressure_in_atm(),
            after_crash_time=instance.after_crash_time,
        )

        instance.evaporation_duration = rd90.evaporation_duration
        instance.full_contamination_depth = rd90.full_contamination_depth
        instance.angular_size = rd90.angular_size
        instance.possible_contamination_area = rd90.possible_contamination_area
        instance.actual_contamination_area = rd90.actual_contamination_area
        instance.json_calculation = rd90.json
        print('+++++++++++++++++++++++++++++instance.json_calculation %s' % instance.json_calculation)

        print('evaporation_duration %s' % instance.evaporation_duration)

        print('+++++++++++++++++++++++++++++json_calculation %s' % rd90.json)

    if chemical_amount > 1:
        rd90_list = []
        # after_crash_hours = instance.after_crash_time.seconds / 3600



        chemical = kwargs.pop('chemical', None)

        print('kwargs: %s' % kwargs)
        print('instance.weather: %s' % instance.weather)
        dovsoa = instance.weather.dovsoa
        # print('dovsoa: %s' % dovsoa)
        wind_speed = instance.weather.wind_speed
        air_t = instance.weather.air_t

        for chem in instance.chemical.iterator():
            rd90_list.append(
                calc.RD90(
                    hazard_substance_obj=chem.hazard_substance,
                    substance_amount=chem.substance_amount,
                    embank_height=chem.embank_height,
                    storage_condition=chem.embank_height,
                    weather_dovsoa=dovsoa,
                    weather_wind_speed=wind_speed,
                    weather_air_t=air_t,
                    weather_atmospheric_pressure=instance.weather.get_atmospheric_pressure_in_atm(),
                    after_crash_time=instance.after_crash_time
                )
            )

        rd90_full = calc.RD90FullCrash(
            weather_dovsoa=dovsoa,
            weather_wind_speed=wind_speed,
            rd90_list=rd90_list,
            after_crash_time=instance.after_crash_time,
        )

        instance.evaporation_duration = rd90_full.evaporation_duration
        instance.full_contamination_depth = rd90_full.contamination_depth
        instance.angular_size = rd90_full.angular_size
        instance.possible_contamination_area = rd90_full.possible_contamination_area
        instance.actual_contamination_area = rd90_full.actual_contamination_area
        print('instance %s ' % instance.__dict__)

        # instance_json = serializers.serialize("json", instance)

        instance.json_calculation = ''
        instance_dict = instance.__dict__

        d = dict((k, v) for k, v in instance_dict.items()
                 if k not in ['_state', 'json_calculation', 'chemical', 'evaporation_duration', 'k1237',
                              'after_crash_time', 'crash_dtime'])
        print(d)
        instance.json_calculation = d
        # json.dumps(d, indent=4, sort_keys=True, ensure_ascii=False)
    instance.save()

# @receiver(pre_save, sender=Rd90Calc)
# def calc_rd90(sender, instance, **kwargs):
#     print("+++++++++++++++++++++++++++++++++++++Signal catched !")
#     chemical_amount = instance.chemical.count()
#     print('chemical_amount: %s' % chemical_amount)
#
#     if chemical_amount == 1:
#         # rd90 = calc.RD90(instance, instance.chemical.first())
#         chem = instance.chemical.first()
#         print('chemical: %s' % chem)
#         rd90 = ''
#         rd90 = calc.RD90(
#             hazard_substance_obj=chem.hazard_substance,
#             substance_amount=chem.substance_amount,
#             embank_height=chem.embank_height,
#             storage_condition=chem.embank_height,
#             weather_dovsoa=instance.weather.dovsoa,
#             weather_wind_speed=instance.weather.wind_speed,
#             weather_air_t=instance.weather.air_t,
#             weather_atmospheric_pressure=instance.weather.get_atmospheric_pressure_in_atm(),
#             after_crash_time=instance.after_crash_time,
#         )
#
#         instance.evaporation_duration = rd90.evaporation_duration
#         instance.full_contamination_depth = rd90.full_contamination_depth
#         instance.angular_size = rd90.angular_size
#         instance.possible_contamination_area = rd90.possible_contamination_area
#         instance.actual_contamination_area = rd90.actual_contamination_area
#         instance.json_calculation = rd90.json
#         print('+++++++++++++++++++++++++++++instance.json_calculation %s' % instance.json_calculation)
#
#         print('evaporation_duration %s' % instance.evaporation_duration)
#
#         print('+++++++++++++++++++++++++++++json_calculation %s' % rd90.json)
#
#     if chemical_amount > 1:
#         rd90_list = []
#         # after_crash_hours = instance.after_crash_time.seconds / 3600
#
#
#
#         chemical = kwargs.pop('chemical', None)
#
#         print('kwargs: %s' % kwargs)
#         print('instance.weather: %s' % instance.weather)
#         dovsoa = instance.weather.dovsoa
#         # print('dovsoa: %s' % dovsoa)
#         wind_speed = instance.weather.wind_speed
#         air_t = instance.weather.air_t
#
#         for chem in instance.chemical.iterator():
#             rd90_list.append(
#                 calc.RD90(
#                     hazard_substance_obj=chem.hazard_substance,
#                     substance_amount=chem.substance_amount,
#                     embank_height=chem.embank_height,
#                     storage_condition=chem.embank_height,
#                     weather_dovsoa=dovsoa,
#                     weather_wind_speed=wind_speed,
#                     weather_air_t=air_t,
#                     weather_atmospheric_pressure=instance.weather.get_atmospheric_pressure_in_atm(),
#                     after_crash_time=instance.after_crash_time
#                 )
#             )
#
#         rd90_full = calc.RD90FullCrash(
#             weather_dovsoa=dovsoa,
#             weather_wind_speed=wind_speed,
#             rd90_list=rd90_list,
#             after_crash_time=instance.after_crash_time,
#         )
#
#         instance.evaporation_duration = rd90_full.evaporation_duration
#         instance.full_contamination_depth = rd90_full.contamination_depth
#         instance.angular_size = rd90_full.angular_size
#         instance.possible_contamination_area = rd90_full.possible_contamination_area
#         instance.actual_contamination_area = rd90_full.actual_contamination_area
#         print('instance %s ' % instance.__dict__)
#
#         # instance_json = serializers.serialize("json", instance)
#
#         instance.json_calculation = ''
#         instance_dict = instance.__dict__
#
#         d = dict((k, v) for k, v in instance_dict.items()
#                  if k not in ['_state', 'json_calculation', 'chemical', 'evaporation_duration', 'k1237',
#                               'after_crash_time', 'crash_dtime'])
#         print(d)
#         instance.json_calculation = d
#         # json.dumps(d, indent=4, sort_keys=True, ensure_ascii=False)
#     # instance.save()



# m2m_changed.connect(handle_flow, sender=Rd90Calc.chemical.through)


# @receiver(m2m_changed, sender=Rd90Calc.chemical.through) #pre_save, sender=Rd90Calc)
# def calc_rd90(sender, instance, **kwargs):
#     chemical_amount = instance.chemical.count()
#     print('chemical_amount: %s' % chemical_amount)
#
#     if chemical_amount == 1:
#         rd90 = calc.RD90(instance, instance.chemical.first())
#         instance.evaporation_duration = rd90.evaporation_duration
#         instance.full_contamination_depth = rd90.full_contamination_depth
#         instance.angular_size = rd90.angular_size
#         instance.possible_contamination_area = rd90.possible_contamination_area
#         instance.actual_contamination_area = rd90.actual_contamination_area
#         instance.json_calculation = rd90.json
#         print('evaporation_duration %s' % instance.evaporation_duration)
#
#     if chemical_amount > 1:
#         rd90_list = []
#         after_crash_hours = instance.after_crash_time.seconds / 3600
#
#         chemical = kwargs.pop('chemical', None)
#         print('kwargs: %s' % kwargs)
#         print('chemical: %s' % chemical)
#
#         for chemical in instance.chemical.iterator():
#             rd90_list.append(calc.RD90(instance, chemical))
#
#         instance.evaporation_duration = max(
#             [rd90.evaporation_duration for rd90 in rd90_list]
#         )
#
#         equivalent_amount = calc.RD90.get_full_equivalent_amount(
#             wind_speed=instance.weather.wind_speed,
#             dovsoa=instance.weather.dovsoa,
#             rd90_list=rd90_list,
#         )
#         contamination_depth = calc.RD90.get_contamination_depth(
#             equivalent_amount=equivalent_amount,
#             wind_speed=instance.weather.wind_speed,
#         )
#         front_speed = calc.RD90.get_front_speed(
#             wind_speed=instance.weather.wind_speed,
#             dovsoa=instance.weather.dovsoa,
#         )
#         possible_contamination_depth = calc.RD90.get_possible_contamination_depth(
#             front_speed=front_speed,
#             after_crash_time=after_crash_hours,
#         )
#         instance.full_contamination_depth = min(contamination_depth, possible_contamination_depth)
#         instance.angular_size = calc.RD90.get_angular_size(wind_speed=instance.weather.wind_speed)
#         instance.possible_contamination_area = calc.RD90.get_possible_contamination_area(
#             contamination_depth=contamination_depth,
#             angular_size=instance.angular_size,
#         )
#         instance.actual_contamination_area = calc.RD90.get_actual_contamination_area(
#             contamination_depth=contamination_depth,
#             dovsoa=instance.weather.dovsoa,
#             after_crash_time=after_crash_hours,
#         )
#         print('instance %s ' % instance.__dict__)
#
#         # instance_json = serializers.serialize("json", instance)
#
#         instance.json_calculation = ''
#         instance_dict = instance.__dict__
#
#         d = dict((k, v) for k, v in instance_dict.items()
#                  if k not in ['_state', 'json_calculation', 'chemical', 'evaporation_duration', 'k1237', 'after_crash_time'])
#         print(d)
#         instance.json_calculation = json.dumps(d, indent=4, sort_keys=True, ensure_ascii=False)





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