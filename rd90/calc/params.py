import sympy
# degree of vertical stability of air
# db_dovsoa = SqliteDatabase('files/dovsoa.db')
from playhouse.reflection import *
import re
# from k1237 import *

from hazard_substance.models import HazardousChemical


import math
import numpy
from datetime import datetime, date, timedelta
from scipy.interpolate import interp1d


class Coeff:
    k1237 = ''  # таблица коэффициентов и характеристик АХОВ П2
    k1 = ''     # К1 - коэффициент, зависящий от условий хранения АХОВ, для сжатых газов К1 = 1
    # значения К1 для изотермического хранения аммиака приведено для случая разлива (выброса) в поддон.
    k2 = ''     # K2 -коэффициент, зависящий от физико-химических свойств АХОВ, удельная скорость испарения
    k3 = ''     # K3 - коэффициент, равный отношению пороговой токсодозы хлора к пороговой токсодозе другого АХОВ
    k4 = ''     # K4 - коэффициент, учитывающий скорость ветра
    k5 = ''     # K5 - коэффициент, учитывающий степень вертикальной устойчивости атмосферы
    k6 = ''     # K6 - коэффициент, зависящий от времени N, прошедшего после начала аварии;
    k7 = ''     # K7 - коэффициент, учитывающий влияние температуры воздуха

    density = '' # плотность АХОВ, плотности газообразных СДЯВ gas_density приведены для атмосферного давления; при давлении в емкости,
    # отличном от атмосферного, плотности определяются путем умножения данных графы 3 на значение
    # давления в атмосферах (1 атм = 760 мм рт. ст.).
    pallet_height = '' # глубина поддона. При проливе в поддон или обваловку
    layer_thickness = '' # толщина слоя разлившегося АХОВ
    evaporation_duration = 0 # продолжительность испарения АХОВ int
     # высота обваловки

    def __init__(self, hcs_id, wind_speed, dovsoa, air_t, after_crash_time=timedelta(hours=1), hcs_storage='gas_under_pressure',
                 cloud=1, spillage='free_spillage', embank_height=0, atmospheric_pressure=1):
        self.k1237 = K1237.get(K1237.id == hcs_id)
        self.k1 = self.get_k1(hcs_storage)
        self.k2 = self.k1237.k2
        self.k3 = self.k1237.k3
        self.k4 = self.get_k4(wind_speed)
        self.k5 = self.get_k5(dovsoa)
        self.k7 = self.get_k7(air_t, cloud, hcs_storage)
        self.density = self.get_density(atmospheric_pressure, hcs_storage)
        self.layer_thickness = self.get_layer_thickness(spillage, embank_height)

        self.k6 = 0 if cloud == 1 else self.get_k6(after_crash_time)


    def get_k1(self, hcs_storage):
        # hcs - hazardous chemical substance
        # hcs_storage - 'gas_under_pressure' || 'no_pressure'
        # К1 - коэффициент, зависящий от условий хранения АХОВ, для сжатых газов К1 = 1
        # Значения К1 для изотермического хранения аммиака приведено для случая разлива (выброса) в поддон.
        # для сжатых газов К1 = 1
        k1 = self.k1237.k1
        if hcs_storage == 'gas_under_pressure':
            k1 = 1
        return k1

    def get_k4(self, wind_speed):
        x = (math.ceil(wind_speed))
        k4 = numpy.interp(x, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15],
                          [1, 1.33, 1.67, 2.0, 2.34, 2.67, 3.0, 3.34, 3.67, 4.0, 5.68])
        return k4



    def get_k6(self, after_crash_time):
        # К6 - коэффициент, зависящий от времени after_crash_time, прошедшего после начала аварии;
        # значение коэффициента К6 определяется после расчета продолжительности evaporation_duration (ч) испарения вещества
        # after_crash_time - время, прошедшее после начала аварии
        # evaporation duration  - продолжительность испарения вещества
        self.evaporation_duration = round((self.layer_thickness * self.density / (self.k2 * self.k4 * self.k7)), 3)
        evaporation_delta = timedelta(hours=self.evaporation_duration)

        delta = timedelta(hours=1)

        #  h - высота слоя разлившегося АХОВ
        if after_crash_time < delta:
            k6 = 1
        if after_crash_time < evaporation_delta:
            after_crash_time_f = after_crash_time.seconds / 3600
            k6 = after_crash_time_f ** 0.8
        if after_crash_time >= evaporation_delta:
            k6 = self.evaporation_duration ** 0.8
        return k6


    def get_k7(self, air_t, cloud=1, hcs_storage='gas_no_pressure'):
        # К7 - коэффициент, учитывающий влияние температуры воздуха (приложение 3; для сжатых газов К7 = 1);
        # cloud = 1, 2 - первичное, вторичное облако
        # коэффициент, учитывающий влияние температуры воздуха ; для сжатых газов К7 = 1;
        # value_list = list(zip([-40, -20, 0, 20, 40], eval(val_list)))
        x = float(air_t)
        if hcs_storage == 'gas_under_pressure':
            return 1
        if cloud == 1:
            # print(self.k1237.k7_1_f)
            # k7_list = eval(self.k1237.k7_1_f)
            k7_list = eval(self.k1237.k7_1)
        elif cloud == 2:
            if self.k1237.k7_2:
                # k7_list = eval(self.k1237.k7_2_f)
                k7_list = eval(self.k1237.k7_2)
            else:
                # k7_list = eval(self.k1237.k7_1_f)
                k7_list = eval(self.k1237.k7_1)
        if isinstance(k7_list, list):
            inter_func = interp1d([-40, -20, 0, 20, 40], k7_list)
            val_list = dict(zip([-40, -20, 0, 20, 40], k7_list))
            if air_t < -40:
                k7 = val_list[-40]
            elif air_t > 40:
                k7 = val_list[40]
            else:
                k7 = inter_func(air_t)
            return k7
        else:
            return None

    def get_density(self, atmospheric_pressure, hcs_storage):
        # Плотности газообразных СДЯВ gas_density приведены для атмосферного давления; при давлении в емкости,
        # отличном от атмосферного, плотности определяются путем умножения данных графы 3 на значение
        # давления в атмосферах (1 атм = 760 мм рт. ст.).
        if hcs_storage == 'liquid':
            return float(self.k1237.liquid_density) * float(atmospheric_pressure)
        else:
            if self.k1237.gas_density:
                return float(self.k1237.gas_density) * float(atmospheric_pressure)

    def get_layer_thickness(self, spillage, embank_height = 0):
        """
        Получение толщины слоя жидкости
        embank_height - высота поддона или обваловки
        Толщина h слоя жидкости для АХОВ, разлившихся свободно на подстилающей поверхности,
        принимается равной 0,05 м по всей площади разлива; для СДЯВ, разлившихся в поддон или обваловку,
        определяется следующим образом:
        а) при разливах из емкостей, имеющих самостоятельный поддон (обваловку): h = H - 0,2,
        где H - высота поддона (обваловки), м;

        :param spillage:
        :param embank_height:
        :return:
        """
        if spillage=='pallet_spillage':
            layer_thickness = embank_height - 0.2
        if spillage=='free_spillage':
            layer_thickness = 0.05
        return layer_thickness

def get_substance_mount(substance_mount, k1237):
    # При авариях на хранилищах сжатого газа - substance_mount - это объем хранилища
    # При авариях на хранилищах сжатого газа Q0 рассчитывается по формуле Q0 = d*Vх
    return substance_mount * k1237.gas_density if k1237.gas_density else substance_mount





if __name__ == '__main__':

    # db.create_tables([K1237], safe=True)
    print(K1237._meta.fields)
    print(K1237.__class__.__name__)
    # params_list = list_from_xlsx('files/tab p2.xlsx')
    # params_source = [get_str_K1237(row) for row in params_list]
    # print(params_source)
    # k2 = K1237.get(K1237.id==1).k2
    k1237 = K1237.get(K1237.id == 1)
    print(k1237.k2, k1237.k3)

    # print('k4 %s:' % get_k4(13))

    # with db.atomic():
    #     K1237.insert_many(params_source).execute()
