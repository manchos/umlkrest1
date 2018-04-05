import numpy
from datetime import datetime, date, timedelta
from scipy.interpolate import interp1d, interp2d
import math
import json


class RD90:
    k1237 = ''  # таблица коэффициентов и характеристик АХОВ П2
    hc_storage = ''  # способ хранения АХОВ
    dovsoa = ''  # cтепень вертикальной устойчивости воздуха
    wind_speed = ''
    layer_thickness = ''  # толщина слоя разлившегося АХОВ
    embank_height = 0.0   # глубина поддона/обваловки. При проливе в поддон или обваловку (м)
    layer_thickness = ''  # толщина слоя разлившегося АХОВ
    evaporation_duration = 0  # продолжительность испарения АХОВ int, вычисляется для k7 2 облака
    density = ''  # плотность АХОВ, плотности газообразных СДЯВ gas_density приведены для атмосферного давления; при давлении в емкости,
    # отличном от атмосферного, плотности определяются путем умножения данных графы 3 на значение
    # давления в атмосферах (1 атм = 760 мм рт. ст.).
    substance_amount = ''  # количество вещества
    after_crash_time = ''  # время после аварии (секунд)
    contamination_depth_1 = ''  # глубина зоны заражения для первичного облака Г1 (км)
    contamination_depth_2 = ''  # глубина зоны заражения для вторичного облака Г2 (км)
    full_contamination_depth = ''  # полная глубина зоны заражения
    front_speed = ''  # предельно возможное значение глубины переноса воздушных масс Гп
    angular_size = ''  # угловой размер зоны возможного заражения (град)
    possible_contamination_area = ''  # возможная площадь зоны возможного заражения АХОВ
    actual_contamination_area = ''  # фактическая площадь зоны возможного заражения АХОВ
    json = ''



    k1 = ''  # коэффициент, зависящий от условий хранения АХОВ, для сжатых газов К1 = 1
    # значения К1 для изотермического хранения аммиака приведено для случая разлива (выброса) в поддон.
    k2 = ''  # коэффициент, зависящий от физико-химических свойств АХОВ, удельная скорость испарения
    k3 = ''  # коэффициент, равный отношению пороговой токсодозы хлора к пороговой токсодозе другого АХОВ
    k4 = ''  # коэффициент, учитывающий скорость ветра
    k5 = ''  # коэффициент, учитывающий степень вертикальной устойчивости атмосферы
    k6 = ''  # коэффициент, зависящий от времени N, прошедшего после начала аварии, вычисляется для 2 облака
    k7_1 = ''  # коэффициент, учитывающий влияние температуры воздуха, вычисляется для 1 облака
    k7_2 = ''  # коэффициент, учитывающий влияние температуры воздуха, вычисляется для 2 облака

    equivalent_amount_1 = ''
    equivalent_amount_2 = ''

    def __init__(self, rd90calc):

        self.k1237 = rd90calc.chemical.hazard_substance
        self.after_crash_time = rd90calc.after_crash_time

        self.embank_height = rd90calc.chemical.embank_height
        self.hc_storage = rd90calc.chemical.hc_storage
        self.dovsoa = rd90calc.weather.dovsoa
        self.wind_speed = rd90calc.weather.wind_speed
        self.substance_amount = rd90calc.chemical.substance_amount
        self.gas_density = self.k1237.gas_density

        print('substance %s' % self.substance_amount)

        self.density = self.get_density(
            atmospheric_pressure=rd90calc.weather.get_atmospheric_pressure_in_atm(),
            hc_storage=self.hc_storage,
            liquid_density=self.k1237.liquid_density,
            gas_density=self.gas_density,
        )

        self.layer_thickness = self.get_layer_thickness(
            embank_height=self.embank_height
        )
        self.k1 = self.k1237.get_k1(hc_storage=self.hc_storage)
        self.k2 = self.k1237.k2
        self.k3 = self.k1237.k3
        self.k4 = self.get_k4(wind_speed=self.wind_speed)
        self.k5 = self.get_k5(dovsoa=self.dovsoa)

        # k7 - вычисляются для 1 и 2 облака отдельно
        self.k7_1 = self.get_k7(
            air_t=rd90calc.weather.air_t,
            func_k7_1=self.k1237.k7_1,
            func_k7_2=self.k1237.k7_2,
            cloud_number=1,
            hc_storage=self.hc_storage,
        )
        self.evaporation_duration = self.get_evaporation_duration(
            layer_thickness=self.layer_thickness,
            density=self.density,
            k2=self.k2,
            k4=self.k4,
            k7=self.k7_1,
        )
        self.k6 = self.get_k6(
            after_crash_time=self.after_crash_time,
            evaporation_duration=self.evaporation_duration,
            cloud_number=2,
        )
        self.k7_2 = self.get_k7(
            air_t=rd90calc.weather.air_t,
            func_k7_1=self.k1237.k7_1,
            func_k7_2=self.k1237.k7_2,
            cloud_number=2,
            hc_storage=self.hc_storage,
        )

        self.substance_amount = self.get_substance_mount(
            substance_mount=self.substance_amount,
            gas_density=self.gas_density,
            hc_storage=self.hc_storage,
        )

        self.equivalent_amount_1 = self.get_equivalent_amount(
            k1=self.k1,
            k3=self.k3,
            k5=self.k5,
            k7=self.k7_1,
            substance_mount=self.substance_amount,
            cloud=1,
        )

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

        self.contamination_depth_1 = self.get_contamination_depth(
            equivalent_amount=self.equivalent_amount_1,
            wind_speed=self.wind_speed
        )

        self.contamination_depth_2 = self.get_contamination_depth(
            equivalent_amount=self.equivalent_amount_2,
            wind_speed=self.wind_speed
        )
        self.front_speed = self.get_front_speed(
            wind_speed=self.wind_speed,
            dovsoa=self.dovsoa,
        )
        self.full_contamination_depth = self.get_full_contamination_depth(
            contamination_depth_1=self.contamination_depth_1,
            contamination_depth_2=self.contamination_depth_2,
            front_speed=self.front_speed,
            after_crash_time=self.after_crash_time.seconds/3600
        )

        self.angular_size = self.get_angular_size(self.wind_speed)
        self.possible_contamination_area = self.get_possible_contamination_area(
            contamination_depth=self.full_contamination_depth,
            angular_size=self.angular_size
        )
        self.actual_contamination_area = self.get_actual_contamination_area(
            contamination_depth=self.full_contamination_depth,
            dovsoa=self.dovsoa,
            after_crash_time=self.after_crash_time.seconds/3600
        )
        print(self.__dict__)
        d = dict((k, v) for k, v in self.__dict__.items() if k not in ['evaporation_duration', 'k1237', 'after_crash_time'])
        print(d)
        self.json = json.dumps(d, indent=4, sort_keys=True, ensure_ascii=False)

        print(self.json)

    def get_density(self, atmospheric_pressure, hc_storage, liquid_density, gas_density):
        # Плотности газообразных СДЯВ gas_density приведены для атмосферного давления; при давлении в емкости,
        # отличном от атмосферного, плотности определяются путем умножения данных графы 3 на значение
        # давления в атмосферах (1 атм = 760 мм рт. ст.).
        if hc_storage == 'liquid':
            return float(liquid_density) * float(atmospheric_pressure)
        else:
            if gas_density:
                return float(gas_density) * float(atmospheric_pressure)

    def get_layer_thickness(self, embank_height):
        """
        Получение толщины слоя жидкости
        embank_height - высота поддона или обваловки
        Толщина h слоя жидкости для АХОВ, разлившихся свободно на подстилающей поверхности,
        принимается равной 0,05 м по всей площади разлива; для СДЯВ, разлившихся в поддон или обваловку,
        определяется следующим образом:
        а) при разливах из емкостей, имеющих самостоятельный поддон (обваловку): h = H - 0,2,
        где H - высота поддона (обваловки), м;

        :param embank_height:
        :return:
        """
        return 0.05 if embank_height == 0 else (embank_height - 0.2)

    def get_k4(self, wind_speed):
        x = (math.ceil(wind_speed))
        k4 = numpy.interp(x, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15],
                          [1, 1.33, 1.67, 2.0, 2.34, 2.67, 3.0, 3.34, 3.67, 4.0, 5.68])
        return k4

    def get_evaporation_duration(self, layer_thickness, density, k2, k4, k7):
        in_hours = round(
            (layer_thickness * density / (k2 * k4 * k7)),
            5
        )
        minutes = round(math.modf(in_hours)[0], 2) * 100
        hours = math.modf(in_hours)[1]
        print('hours %s' % hours)
        print('minutes  %s' % minutes)
        return timedelta(hours=hours, minutes=minutes)


    # плотность АХОВ, плотности газообразных СДЯВ gas_density

    def get_k5(self, dovsoa):
        # коэффициент, учитывающий степень вертикальной устойчивости воздуха
        if dovsoa == 'ин':
            return 1
        if dovsoa == 'из':
            return 0.23
        if dovsoa == 'к':
            return 0.08

    def get_k6(self, after_crash_time, evaporation_duration, cloud_number):
        # К6 - коэффициент, зависящий от времени after_crash_time, прошедшего после начала аварии;
        # значение коэффициента К6 определяется после расчета
        # продолжительности evaporation_duration (ч) испарения вещества
        # after_crash_time - время, прошедшее после начала аварии (timedelta)
        # evaporation duration  - продолжительность испарения вещества
        if cloud_number == 1:
            return 0
        # evaporation_delta = timedelta(hours=evaporation_duration)


        evaporation_delta = evaporation_duration
        delta = timedelta(hours=1)
        #  h - высота слоя разлившегося АХОВ
        if after_crash_time < delta:
            k6 = 1
        if after_crash_time < evaporation_delta:
            after_crash_time_f = after_crash_time.seconds / 3600
            k6 = after_crash_time_f ** 0.8
        if after_crash_time >= evaporation_delta:
            k6 = (evaporation_duration.seconds/3600) ** 0.8
        return k6

    def get_k7(self, air_t, func_k7_1, func_k7_2, cloud_number=1, hc_storage='gas_no_pressure'):
        # К7 - коэффициент, учитывающий влияние температуры воздуха (приложение 3; для сжатых газов К7 = 1);
        # cloud_number = 1, 2 - первичное, вторичное облако
        # коэффициент, учитывающий влияние температуры воздуха ; для сжатых газов К7 = 1;
        # value_list = list(zip([-40, -20, 0, 20, 40], eval(val_list)))
        if hc_storage == 'gas_under_pressure':
            return 1
        if cloud_number == 1:
            # print(self.k1237.k7_1_f)
            # k7_list = eval(self.k1237.k7_1_f)
            k7_list = eval(func_k7_1)
        elif cloud_number == 2:
            if self.k1237.k7_2:
                # k7_list = eval(self.k1237.k7_2_f)
                k7_list = eval(func_k7_2)
            else:
                # k7_list = eval(self.k1237.k7_1_f)
                k7_list = eval(func_k7_1)
        if isinstance(k7_list, list):
            inter_func = interp1d([-40, -20, 0, 20, 40], k7_list)
            val_list = dict(zip([-40, -20, 0, 20, 40], k7_list))
            if air_t < -40:
                k7 = val_list[-40]
            elif air_t > 40:
                k7 = val_list[40]
            else:
                k7 = inter_func(air_t)
            return k7.__abs__()
        else:
            return None

    def get_substance_mount(self, substance_mount, gas_density, hc_storage):
        # При авариях на хранилищах сжатого газа - substance_mount - это объем хранилища
        # При авариях на хранилищах сжатого газа Q0 рассчитывается по формуле Q0 = d*Vх
        if hc_storage == 'liquid':
            return substance_mount
        return substance_mount * gas_density if gas_density else substance_mount

    # Определение эквивалентного количества вещества в первичном облаке и вторичном облаке
    def get_equivalent_amount(
            self, k1, k3, k5, k7, substance_mount, cloud,
            k2=0, k4=0, k6=0, layer_thickness=0.0, density=0.0):
        if cloud == 1:
            return k1 * k3 * k5 * k7 * substance_mount
        if cloud == 2:
            return ((1 - k1) * k2 * k3 * k4 * k5 * k6 * k7 * substance_mount /
                    (layer_thickness * density))


    # Глубина зоны заражения км.
    def get_contamination_depth(self, equivalent_amount, wind_speed):
        '''
        :param equivalent_amount:
        :param wind_speed:
        :return:
        '''
        x = [0.01, 0.05, 0.1, 0.5, 1, 3, 5, 10, 20, 30, 50, 70, 100, 300, 500, 700, 1000, 2000]
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        z = [
            [0.38, 0.85, 1.25, 3.16, 4.75, 9.18, 12.53, 19.20, 29.56, 38.13, 52.67, 65.23, 81.91, 166, 231, 288, 363, 572],
            [0.26, 0.59, 0.84, 1.92, 2.84, 5.35, 7.20, 10.83, 16.44, 21.02, 28.73, 35.35, 44.09, 87.79, 121, 150, 189, 295],
            [0.22, 0.48, 0.68, 1.53, 2.17, 3.99, 5.34, 7.96, 11.94, 15.18, 20.59, 25.21, 31.30, 61.47, 84.50, 104, 130, 202],
            [0.19, 0.42, 0.59, 1.33, 1.88, 3.28, 4.36, 6.46, 9.62, 12.18, 16.43, 20.05, 24.80, 48.18, 65.92, 81.17, 101, 157],
            [0.17, 0.38, 0.53, 1.19, 1.68, 2.91, 3.75, 5.53, 8.19, 10.33, 13.88, 16.89, 20.82, 40.11, 54.67, 67.15, 83.60, 129],
            [0.15, 0.34, 0.48, 1.09, 1.53, 2.66, 3.43, 4.88, 7.20, 9.06, 12.14, 14.79, 18.13, 34.67, 47.09, 56.72, 71.70, 110],
            [0.14, 0.32, 0.45, 1.00, 1.42, 2.46, 3.17, 4.49, 6.48, 8.14, 10.87, 13.17, 16.17, 30.73, 41.63, 50.93, 63.16, 96.30],
            [0.13, 0.30, 0.42, 0.94, 1.33, 2.30, 2.97, 4.20, 5.92, 7.42, 9.90, 11.98, 14.68, 27.75, 37.49, 45.79, 56.70, 86.20],
            [0.12, 0.28, 0.40, 0.88, 1.25, 2.17, 2.80, 3.96, 5.60, 6.86, 9.12, 11.03, 13.50, 25.39, 34.24, 41.76, 51.60, 78.30],
            [0.12, 0.26, 0.38, 0.84, 1.19, 2.06, 2.66, 3.76, 5.31, 6.50, 8.50, 10.23, 12.54, 23.49, 31.61, 38.50, 47.53, 71.90],
            [0.11, 0.25, 0.36, 0.80, 1.13, 1.96, 2.53, 3.58, 5.06, 6.20, 8.01, 9.61, 11.74, 21.91, 29.44, 35.81, 44.15, 66.62],
            [0.11, 0.24, 0.34, 0.76, 1.08, 1.88, 2.42, 3.43, 4.85, 5.94, 7.67, 9.07, 11.06, 20.58, 27.61, 35.55, 41.30, 62.20],
            [0.10, 0.23, 0.33, 0.74, 1.04, 1.80, 2.37, 3.29, 4.66, 5.70, 7.37, 8.72, 10.48, 19.45, 26.04, 31.62, 38.90, 58.44],
            [0.10, 0.22, 0.32, 0.71, 1.00, 1.74, 2.24, 3.17, 4.49, 5.50, 7.10, 8.40, 10.04, 18.46, 24.69, 29.95, 36.81, 55.20],
            [0.10, 0.22, 0.31, 0.69, 0.97, 1.68, 2.17, 3.07, 4.34, 5.31, 6.86, 8.11, 9.70, 17.60, 23.50, 28.48, 34.98, 52.37]
        ]
        f = interp2d(x, y, z, kind='linear')
        return f(equivalent_amount, wind_speed)[0]

    # нахождение скорости переноса переднего фронта зараженного воздуха при данной скорости ветра
    # и степени вертикальной устойчивости воздуха, км/ч
    def get_front_speed(self, wind_speed, dovsoa):
        '''
        нахождение скорости переноса переднего фронта зараженного воздуха при данной скорости ветра и степени
        вертикальной устойчивости воздуха, км/ч (таблица).
        :param wind_speed: скорость ветра м/с
        :param dovsoa: состояние атмосферы (степень вертикальной устойчивости)
        :return: скорость переноса переднего фронта облака зараженного воздуха в зависимости от скорости ветра
        '''
        wind_speed_i = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        print('wind speed %s ' % wind_speed)
        invers_speed = [0, 5, 10, 16, 21]
        konvek_speed = [0, 7, 14, 21, 28]
        isoterm_speed = [6, 12, 18, 24, 29, 35, 41, 47, 53, 59, 65, 71, 76, 82, 88]
        value_list = list(zip(wind_speed_i, isoterm_speed))
        if dovsoa == 'из':
            f = interp1d(wind_speed_i, isoterm_speed, bounds_error=False, fill_value="extrapolate")
            return f(wind_speed).__abs__()
        wind_speed = int(wind_speed)
        if dovsoa == 'ин' and wind_speed in range(1, 4):
            return invers_speed[wind_speed]
        if dovsoa == 'к' and wind_speed in range(1, 4):
            return konvek_speed[wind_speed]

    # Определение полной глубины зоны заражения Г (км)
    def get_full_contamination_depth(self, contamination_depth_1, contamination_depth_2, front_speed, after_crash_time):
        '''
        :param contamination_depth_1:
        :param contamination_depth_2:
        :param front_speed:
        :param after_crash_time:
        :return:
        Полная глубина зоны заражения Г (км), обусловленной воздействием первичного и вторичного облака СДЯВ,
        определяется: Г = Г‘ + 0,5Г“, где Г‘ - наибольший, Г“ - наименьший из размеров Г1 и Г2.
        Полученное значение сравнивается с предельно возможным значением глубины переноса
        воздушных масс Гп, определяемым по формуле:
        Гп = Nv, где N - время от начала аварии, ч;
        v- скорость переноса переднего фронта
        зараженного воздуха при данной скорости ветра и степени вертикальной устойчивости воздуха, км/ч
        За окончательную расчетную глубину зоны заражения принимается меньшее из двух
        сравниваемых между собой значений.
        '''
        max_contamination_depth = max(contamination_depth_1, contamination_depth_2) + \
                                  0.5 * min(contamination_depth_1, contamination_depth_2)
        possible_depth = front_speed * after_crash_time
        return min(max_contamination_depth, possible_depth)

    def get_angular_size(self, wind_speed):
        '''
        :param wind_speed: (м/с)
        :return: Значение углового размера зоны заражения (град)
        '''
        if wind_speed <= 0.5:
            fi = 360
        elif 0.6 <= wind_speed <= 1:
            fi = 180
        elif 1.1 <= wind_speed <= 2:
            fi = 90
        elif wind_speed > 2:
            fi = 45
        return fi

    def get_possible_contamination_area(self, contamination_depth, angular_size):
        '''
        :param contamination_depth:
        :param wind_speed:
        :return: площадь зоны возможного заражения АХОВ при времени испарения не более 4 часов (квадр. км)
        '''
        fi = angular_size
        contamination_area = (math.pi * contamination_depth ** 2 * fi) / 360
        return contamination_area

    def get_actual_contamination_area(self, contamination_depth, dovsoa, after_crash_time):
        '''
        :param contamination_depth: (км)
        :param dovsoa: ( in 'ин', 'из', 'к' )
        :param after_crash_time: (ч)
        :return: площадь зоны фактического заражения АХОВ  (квадр. км)
        '''
        k8_list = {'ин': 0.081, 'из': 0.133, 'к': 0.235}
        actual_contamination_area = k8_list[dovsoa] * contamination_depth ** 2 * after_crash_time ** 0.2
        return actual_contamination_area




if __name__ == '__main__':
    pass
