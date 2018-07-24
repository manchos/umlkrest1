
from datetime import timedelta

from collections import namedtuple

import rd90.calc.aux as aux

import weather.dovsoa as dovsoa

import weather.meteo_info as meteo_info

#from hazard_substance.models import HazardousChemical

# http://www.gostrf.com/norma_data/45/45344/index.htm#i1918573  - methodic description

HazardousChemical = namedtuple('HazardousChemical',[
    'name',
    'form',
    'gas_density',
    'liquid_density',
    'k1', 'k2', 'k3', 'k7'
])

Weather = namedtuple('Wheather', [
    'wind_speed',
    'wind_direction',
    'air_t',
    'atmospheric_pressure',
    'is_snow',
    'cloud_score',
    'dovsoa',
])

output_data = {
    'evaporation_duration',
    'full_contamination_depth',
}



def rd90(
        chemical=HazardousChemical(
            name=None,
            form=None,
            gas_density=None,
            liquid_density=None,
            k1=None,
            k2=None,
            k3=None,
            k7=None
        ),
        chemical_amount=None,
        storage_kind='gas', # 'liquid' || 'gas' || 'gas_under_pressure'
        weather=Weather(
            wind_speed=1,
            wind_direction=None,
            air_t=None,
            atmospheric_pressure=1,
            is_snow=False,
            cloud_score=None,
            dovsoa=None,
        ),
        after_crash_time=1,
        embank_height = 0, # высота поддона обваловки
        output_data_part=None,
        time_of_day=None,
        crash_datetime=None,
        city_name='Moscow'
    ):

    if not len(output_data_part) == len(output_data_part & output_data):
        return None

    # 1. Qэ1 = К1 К3 К5 К7 Q0,

    if weather.dovsoa is None:

        if time_of_day is None or crash_datetime is None:
            raise Exception("Impossible calculate the degree of vertical stability of the atmosphere (dovsoa)")
        time_of_day = time_of_day if time_of_day else dovsoa.get_time_of_day(crash_datetime, city_name='Moscow')

        weather.dovsoa = dovsoa.get_dovsoa(
            time_of_day=time_of_day,
            wind_speed=weather.wind_speed,
            cloudiness=meteo_info.is_cloudiness(weather.cloud_score),
            snow=weather.is_snow
        )

    k1, k2, k3, k7_json = chemical.k1, chemical.k2, chemical.k3, chemical.k7
    k5 = aux.get_k5(weather.dovsoa)
    k4 = aux.get_k4(weather.wind_speed)
    k7_1 = aux.get_k7(
        air_t=weather.air_t,
        cloud_number=1,
        k7_json=k7_json,
        storage_kind=storage_kind,
    )

    k7_2 = aux.get_k7(
        air_t=weather.air_t,
        cloud_number=2,
        k7_json=k7_json,
        storage_kind=storage_kind,
    )


    chemical_thickness = aux.get_chemical_thickness(embank_height=embank_height)

    density = aux.get_density(
        storage_kind=storage_kind,
        liquid_density=chemical.liquid_density,
        gas_density=chemical.gas_density,
        atmospheric_pressure=weather.atmospheric_pressure,
    )

    evaporation_duration = aux.get_evaporation_duration(
        chemical_thickness=chemical_thickness,
        density=density,
        k2=k2,
        k4=k4,
        k7=k7_2,
    )

    k6 = aux.get_k6(after_crash_time=1, evaporation_duration=evaporation_duration)

    equivalent_amount_cloud1 = aux.get_equivalent_amount(
        k1=k1, k3=k3, k5=k5, k7=k7_1, chemical_amount=chemical_amount, cloud_number=1)

    equivalent_amount_cloud2 = aux.get_equivalent_amount(
        k1=k1, k2=k2, k3=k3, k4=k4, k5=k5, k6=k6, k7=k7_2, cloud_number=2,
        chemical_thickness=chemical_thickness,
        chemical_amount=chemical_amount,
        density=density,
    )








"""

2.1
На химическом предприятии произошла авария на технологическом трубопроводе с жидким хлором, находящимся под давлением.
Количество вытекшей из трубопровода жидкости не установлено.
Известно, что в технологической системе содержалось 40 т сжиженного хлора.
Требуется определить глубину зоны возможного заражения хлором при времени от начала аварии 1 ч и
продолжительность действия источника заражения (время испарения хлора).
Метеоусловия на момент аварии: скорость ветра 5 м/с, температура воздуха 0 °С, изотермия.
Разлив СДЯВ на подстилающей поверхности - свободный.

(Так как количество разлившегося жидкого хлора неизвестно,
то согласно п. 1.5 принимаем его равным максимальному - 40 т.)




{
    source_data = {
        name = Хлор,
        substance_amount = 40,
        after_crash_time = 1,
    },
    weather = {
        wind_speed = 5,
        t = 0,
        dovsoa = 'из'
    }
    output_data = {
        possible_depth,
        evaporation_duration
    }
}


Необходимо оценить опасность возможного очага химического поражения через 1 ч после аварии на химически опасном объекте,
расположенном в южной части города. На объекте в газгольдере емкостью 2000 м3 хранится аммиак.
Температура воздуха 40 °С.
Северная граница объекта находится на расстоянии 200 м от возможного места аварии.
Затем идет 300-метровая санитарно-защитная зона, за которой расположены жилые кварталы.
Давление в газгольдере - атмосферное.


Оценить, на каком расстоянии через 4 ч после аварии будет сохраняться опасность поражения населения в зоне химического
заражения при разрушении изотермического хранилища аммиака емкостью 30000 т.
Высота обваловки емкости 3,5 м. Температура воздуха 20 °С.
(Поскольку метеоусловия и выброс неизвестны, то, согласно п. 1.5 принимается:
метеоусловия - инверсия, скорость ветра - 1 м/с,
выброс равен общему количеству вещества, содержащегося в емкости, - 30000 т.)


На участке аммиакопровода Тольятти - Одесса произошла авария, сопровождавшаяся выбросом аммиака.
Объем выброса не установлен. Требуется определить глубину зоны возможного заражения аммиаком через 2 ч после аварии.
Разлив аммиака на подстилающей поверхности свободный. Температура воздуха 20 °С.
(Так как объем разлившегося аммиака неизвестен, то, согласно п. 1.7,
принимаем его равным 500 т - максимальному количеству,
содержащемуся в трубопроводе между автоматическими отсекателями.
Метеоусловия, согласно п. 1.5, принимаются: инверсия, скорость ветра 1 м/с.)


Пример 2.5
На химически опасном объекте сосредоточены запасы СДЯВ, в том числе хлора - 30 т, аммиака - 150 т,
нитрила акриловой кислоты - 200 т.
Определить глубину зоны заражения в случае разрушения объекта.
Время, прошедшее после разрушения объекта, - 3 ч. Температура воздуха 0 °С.


Пример 3.1
В результате аварии на химически опасном объекте образовалась зона заражения глубиной 10 км.
Скорость ветра составляет 2 м/с, инверсия.
Определить площадь зоны заражения, если после начала аварии прошло 4 ч.


Пример 4.1
В результате аварии на объекте, расположенном на расстоянии 5 км от города, произошло разрушение емкости с хлором.
Метеоусловия: изотермия, скорость ветра 4 м/с. Определить время подхода облака зараженного воздуха к границе города.


Пример 4.2
В результате аварии произошло разрушение обвалованной емкости с хлором.
Требуется определить время поражающего действия СДЯВ.
Метеоусловия на момент аварии: скорость ветра 4 м/с, температура воздуха 0 °С, изотермия. Высота обваловки - 1 м.


"""





class RD90:

    def __call__(
            self,
            hazard_substance_obj,  # HazardousChemical
            substance_amount,
            embank_height,
            storage_condition,
            weather_dovsoa,
            weather_wind_speed,
            weather_air_t,
            weather_atmospheric_pressure, #rd90calc.weather.get_atmospheric_pressure_in_atm(),
            after_crash_time=timedelta(hours=1)
    ):

        self.after_crash_time =after_crash_time

        if isinstance(hazard_substance_obj, HazardousChemical):
            self.hazard_substance = hazard_substance_obj
        else:
            raise TypeError("hazard_substance_obj must be HazardousChemical type")

        self.gas_density = self.hazard_substance.gas_density
        self.substance_amount = substance_amount  # количество вещества
        self.embank_height = embank_height  # глубина поддона/обваловки. При проливе в поддон или обваловку (м)
        self.storage_condition = storage_condition  # способ хранения АХОВ
        self.dovsoa = weather_dovsoa  # cтепень вертикальной устойчивости воздуха
        self.wind_speed = weather_wind_speed  # скорость ветра

        after_crash_hours = after_crash_time.seconds / 3600  #  время после аварии (секунд)


        # плотность АХОВ (т/м3), плотности газообразных СДЯВ gas_density приведены для атмосферного давления;
        # при давлении в емкости, отличном от атмосферного, плотности определяются путем умножения данных графы 3
        #  на значение давления в атмосферах (1 атм = 760 мм рт. ст.)
        self.density = self.get_density(
            atmospheric_pressure=weather_atmospheric_pressure,
            hc_storage=storage_condition,
            liquid_density=self.hazard_substance.liquid_density,
            gas_density=self.gas_density,
        )

        # толщина слоя разлившегося АХОВ
        self.layer_thickness = self.get_layer_thickness(
            embank_height=self.embank_height
        )

        # k1 = ''  # коэффициент, зависящий от условий хранения АХОВ, для сжатых газов К1 = 1
        # значения К1 для изотермического хранения аммиака приведено для случая разлива (выброса) в поддон.
        self.k1 = self.hazard_substance.get_k1(hc_storage=self.storage_condition)

        # k2 = ''  # коэффициент, зависящий от физико-химических свойств АХОВ, удельная скорость испарения
        self.k2 = self.hazard_substance.k2

        # k3 = ''  # коэффициент, равный отношению пороговой токсодозы хлора к пороговой токсодозе другого АХОВ
        self.k3 = self.hazard_substance.k3

        # k4 = ''  # коэффициент, учитывающий скорость ветра
        self.k4 = self.get_k4(wind_speed=self.wind_speed)

        # k5 = ''  # коэффициент, учитывающий степень вертикальной устойчивости атмосферы
        self.k5 = self.get_k5(dovsoa=self.dovsoa)

        # k7 - вычисляются для 1 и 2 облака отдельно
        # k7_1 = ''  # коэффициент, учитывающий влияние температуры воздуха, вычисляется для 1 облака
        self.k7_1 = self.get_k7(
            air_t=weather_air_t,
            func_k7_1=self.hazard_substance.k7_1,
            func_k7_2=self.hazard_substance.k7_2,
            cloud_number=1,
            hc_storage=self.storage_condition,
        )

        # evaporation_duration = 0  # продолжительность испарения АХОВ int, вычисляется для k7 2 облака
        self.evaporation_duration = self.get_evaporation_duration(
            layer_thickness=self.layer_thickness,
            density=self.density,
            k2=self.k2,
            k4=self.k4,
            k7=self.k7_1,
        )

        # k6 = ''  # коэффициент, зависящий от времени N, прошедшего после начала аварии, вычисляется для 2 облака
        self.k6 = self.get_k6(
            after_crash_time=self.after_crash_time,
            evaporation_duration=self.evaporation_duration,
            cloud_number=2,
        )

        # k7_2 = ''  # коэффициент, учитывающий влияние температуры воздуха, вычисляется для 2 облака
        self.k7_2 = self.get_k7(
            air_t=weather_air_t,
            func_k7_1=self.hazard_substance.k7_1,
            func_k7_2=self.hazard_substance.k7_2,
            cloud_number=2,
            hc_storage=self.storage_condition,
        )

        self.substance_amount = self.get_substance_amount(
            substance_amount=self.substance_amount,
            gas_density=self.gas_density,
            hc_storage=self.storage_condition,
        )

        # equivalent_amount_1 = ''  # Эквивалентое количество АХОВ на объекте в первичном облаке
        self.equivalent_amount_1 = self.get_equivalent_amount(
            k1=self.k1,
            k3=self.k3,
            k5=self.k5,
            k7=self.k7_1,
            substance_mount=self.substance_amount,
            cloud=1,
        )

        # equivalent_amount_2 = ''  # Эквивалентое количество АХОВ на объекте во вторичном облаке
        self.equivalent_amount_2 = self.get_equivalent_amount(
            k1=self.k1,
            k3=self.k3,
            k5=self.k5,
            k7=self.k7_2,
            substance_mount=self.substance_amount,
            cloud=2,
            k2=self.k2,
            k4=self.k4,
            k6=self.k6,
            layer_thickness=self.layer_thickness,
            density=self.density
        )

        # contamination_depth_1 = ''  # глубина зоны заражения для первичного облака Г1 (км)
        self.contamination_depth_1 = self.get_contamination_depth(
            equivalent_amount=self.equivalent_amount_1,
            wind_speed=self.wind_speed
        )

        # front_speed = ''  # предельно возможное значение глубины переноса воздушных масс Гп
        self.front_speed = self.get_front_speed(
            wind_speed=self.wind_speed,
            dovsoa=self.dovsoa,
        )

        # contamination_depth_2 = ''  # глубина зоны заражения для вторичного облака Г2 (км)
        self.contamination_depth_2 = self.get_contamination_depth(
            equivalent_amount=self.equivalent_amount_2,
            wind_speed=self.wind_speed,
        )

        # possible_contamination_depth = ''  # Предельно возможное значение глубины переноса воздушных масс (км)
        self.possible_contamination_depth = self.get_possible_contamination_depth(
            front_speed=self.front_speed,
            after_crash_time=after_crash_hours
        )

        # full_contamination_depth = ''  # полная глубина зоны заражения (км)
        self.full_contamination_depth = self.get_full_contamination_depth(
            contamination_depth_1=self.contamination_depth_1,
            contamination_depth_2=self.contamination_depth_2,
            possible_contamination_depth=self.possible_contamination_depth,
        )

        # angular_size = ''  # угловой размер зоны возможного заражения (град)
        self.angular_size = self.get_angular_size(self.wind_speed)

        # possible_contamination_area = ''  # возможная площадь зоны возможного заражения АХОВ
        self.possible_contamination_area = self.get_possible_contamination_area(
            contamination_depth=self.full_contamination_depth,
            angular_size=self.angular_size
        )

        # actual_contamination_area = ''  # фактическая площадь зоны возможного заражения АХОВ
        self.actual_contamination_area = self.get_actual_contamination_area(
            contamination_depth=self.full_contamination_depth,
            dovsoa=self.dovsoa,
            after_crash_time=after_crash_hours
        )

        print('substance %s' % hazard_substance_obj)
        print('substance amount%s' % substance_amount)
        print(self.__dict__)
        d = dict((k, v) for k, v in self.__dict__.items()
                 if k not in ['evaporation_duration', 'hazard_substance', 'after_crash_time', 'crash_dtime'])
        print(d)
        self.json = d
        # json.dumps(d, indent=4, sort_keys=True, ensure_ascii=False)

        # print(self.json)
        return


    # нахождение скорости переноса переднего фронта зараженного воздуха при данной скорости ветра
    # и степени вертикальной устойчивости воздуха, км/ч




    # def calc_for_full_crash(self, k2, k3, k6, k7_2, substance_amount, density):
    #     return k2 * k3 * k6 * k7_2 * (substance_amount / density)

    def calc_for_full_crash(self):
        return self.k2 * self.k3 * self.k6 * self.k7_2 * (self.substance_amount / self.density)

    @classmethod
    def get_full_equivalent_amount(cls, wind_speed, dovsoa, rd90_list):
        return (20 * cls.get_k4(wind_speed) * cls.get_k5(dovsoa) *
                sum(rd90.calc_for_full_crash() for rd90 in rd90_list))


class RD90FullCrash:

    def __init__(self, weather_wind_speed, weather_dovsoa, rd90_list, after_crash_time):
        after_crash_hours = after_crash_time.seconds / 3600

        self.evaporation_duration = max(
            [rd90.evaporation_duration for rd90 in rd90_list]
        )

        self.equivalent_amount = RD90.get_full_equivalent_amount(
            wind_speed=weather_wind_speed,
            dovsoa=weather_dovsoa,
            rd90_list=rd90_list,
        )
        contamination_depth = RD90.get_contamination_depth(
            equivalent_amount=self.equivalent_amount,
            wind_speed=weather_wind_speed,
        )
        front_speed = RD90.get_front_speed(
            wind_speed=weather_wind_speed,
            dovsoa=weather_dovsoa,
        )
        possible_contamination_depth = RD90.get_possible_contamination_depth(
            front_speed=front_speed,
            after_crash_time=after_crash_hours,
        )
        self.contamination_depth = min(contamination_depth, possible_contamination_depth)
        self.angular_size = RD90.get_angular_size(wind_speed=weather_wind_speed)
        self.possible_contamination_area = RD90.get_possible_contamination_area(
            contamination_depth=contamination_depth,
            angular_size=self.angular_size,
        )
        self.actual_contamination_area = RD90.get_actual_contamination_area(
            contamination_depth=contamination_depth,
            dovsoa=weather_dovsoa,
            after_crash_time=after_crash_hours,
        )

    # calc_list = {
    #     'evaporation_duration': evaporation_duration,
    #     'full_equivalent_amount': full_equivalent_amount, # Эквивалентое количество всех АХОВ На объекте
    #     'contamination_depth': contamination_depth,
    #     'possible_contamination_depth': possible_contamination_depth,
    #     'full_contamination_depth': full_contamination_depth,
    #     'angular_size': angular_size,
    #     'possible_contamination_area': possible_contamination_area,
    #     'actual_contamination_area': actual_contamination_area
    # }

    # return calc_list


if __name__ == '__main__':
    pass
