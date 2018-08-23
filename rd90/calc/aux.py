import numpy
from datetime import datetime, date, timedelta
from scipy.interpolate import interp1d
import math
import json
from collections import namedtuple


# def get_k1(k1, storage_kind='gas_under_pressure'):
#     """hcs - hazardous chemical substance
#     storage_kind - 'gas_under_pressure' || 'no_pressure'
#     K1 - коэффициент, зависящий от условий хранения АХОВ, для сжатых газов К1 = 1
#     Значения К1 для изотермического хранения аммиака приведено для случая разлива (выброса) в поддон.
#     для сжатых газов К1 = 1
#     """
#     if storage_kind == 'gas_under_pressure':
#         k1 = 1
#     return k1


def get_k4(wind_speed):
    """
    k4 – коэффициент, учитывающий скорость ветра
    :param wind_speed: float
    :return: float
    """
    k4 = numpy.interp(wind_speed, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15],
                      [1, 1.33, 1.67, 2.0, 2.34, 2.67, 3.0, 3.34, 3.67, 4.0, 5.68])
    return k4


# плотность АХОВ, плотности газообразных АХОВ gas_density
def get_k5(dovsoa):
    """коэффициент, учитывающий степень вертикальной устойчивости воздуха
    dovsoa in ('ин', 'из', 'к')
    """
    dovsoa_dict = {'ин': 1, 'из': 0.23, 'к': 0.08}
    return dovsoa_dict.get(dovsoa, None)



def get_k6(after_crash_time, evaporation_duration):
    """К6 - коэффициент, зависящий от времени after_crash_time, прошедшего после начала аварии;
    значение коэффициента К6 определяется после расчета
    продолжительности evaporation_duration: datetime.delta (ч) испарения вещества
    after_crash_time: datetime.delta - время, прошедшее после начала аварии (timedelta)
    """
    if after_crash_time < timedelta(hours=1):
        after_crash_time = timedelta(hours=1)
    if after_crash_time < evaporation_duration:
        after_crash_time_f = after_crash_time.seconds / 3600
        k6 = after_crash_time_f ** 0.8
    else:
        k6 = (evaporation_duration.seconds/3600) ** 0.8
    return round(float(k6), 4)


def get_k7(air_t=0, cloud_number=1, k7_json='[[0,0,0,0,0],[0,0,0,0,0]]', storage_kind='gas_no_pressure'):
    """
    К7 - коэффициент, учитывающий влияние температуры воздуха (приложение 3; для сжатых газов К7 = 1);
    cloud_number = 1, 2 - первичное, вторичное облако
    коэффициент, учитывающий влияние температуры воздуха ; для сжатых газов К7 = 1;
    :param air_t: int
    :param cloud_number: 1 or 2
    :param k7_json: [[0,0,0,0,0],[0,0,0,0,0]]
    :param storage_kind: str  'gas_no_pressure' || 'gas_under_pressure'
    :return: float
    """
    t_set = (-40, -20, 0, 20, 40)
    k7_list = json.loads(k7_json)
    if cloud_number not in (1, 2):
        return None
    if storage_kind == 'gas_under_pressure':
        return 1
    inter_func = interp1d(t_set, k7_list[cloud_number - 1])
    val_list = dict(zip([-40, -20, 0, 20, 40], k7_list[cloud_number - 1]))
    if air_t < -40:
        k7 = val_list[-40]
    elif air_t > 40:
        k7 = val_list[40]
    else:
        k7 = inter_func(air_t)
    return round(float(k7), 4)


def get_substance_amount(substance_capacity, density, hc_storage, hc_percent=None):
    """
    При авариях на хранилищах сжатого газа (hc_storage == 'gas_under_pressure') 
    Q0 рассчитывается по формуле:
    Q0 = d Vх,.
    где d - плотность АХОВ, т/м3 (приложение 3);
    Vх - объем хранилища, м3.
    
    При авариях на газопроводе (hc_storage == 'gas-pipe') Q0 рассчитывается по формуле:
    Q0 = п d Vг/100	(3)
    где п/hc_percent - содержание АХОВ в природном газе, %;
    d - плотность АХОВ, т/м3 (приложение 3);
    Vг - объем секции газопровода между автоматическими отсекателями, м3.

    :param substance_capacity: float  (cubic meter)
    :param density: float (ton / cubic metr)
    :param hc_storage: str in ('liquid', 'gas-pipe', 'gas_under_pressure')
    :param hc_percent: int (percent)
    :return: float (tons)
    """
    if hc_storage == 'gas-pipe' and hc_percent is not None:
        return substance_capacity * density * hc_percent
    else:
        return substance_capacity * density


# Определение эквивалентного количества вещества в первичном облаке и вторичном облаке
def get_equivalent_amount(
        k1, k3, k5, k7, chemical_amount, cloud_number,
        k2=0.0, k4=0.0, k6=0.0, chemical_thickness=0.0, density=0.0):

    """
    Эквивалентное количество Qэ1 (т) вещества в первичном облаке определяется по формуле:
    Qэ1 = К1 К3 К5 К7 Q0
    :param k1: float коэффициент, зависящий от условий хранения АХОВ (приложение 3; для сжатых газов К1 = 1);
    :param k3: float коэффициент, равный отношению пороговой токсодозы хлора к пороговой токсодозе другого АХОВ (приложение 3);
    :param k5: float
    :param k7: float (k7_1 for cloud_number ==1  and k7_2 for cloud_number == 2)
    :param chemical_amount: float  Q0 - количество выброшенного (разлившегося) при аварии вещества, т.
    :param cloud_number: 1 or 2
    :param k2: float
    :param k4: float
    :param k6: float
    :param chemical_thickness: float
    :param density: float
    :return:
    """
    if cloud_number == 1:
        return k1 * k3 * k5 * k7 * chemical_amount
    if cloud_number == 2:
        return ((1 - k1) * k2 * k3 * k4 * k5 * k6 * k7 *
                chemical_amount / (chemical_thickness * density))


def get_density(storage_kind, liquid_density, gas_density, atmospheric_pressure=1):
    """
    Плотности газообразных АХОВ gas_density приведены для атмосферного давления; при давлении в емкости,
    отличном от атмосферного, плотности определяются путем умножения данных графы 3 на значение
    давления в атмосферах (1 атм = 760 мм рт. ст.).
    :param atmospheric_pressure: float default =1
    :param storage_kind: 'liquid' || 'gas' || 'gas_under_pressure'
    :param liquid_density:
    :param gas_density:
    :return:
    """
    chemical_dencity = {
        'liquid': float(liquid_density),
        'gas_under_pressure': float(gas_density) * float(atmospheric_pressure),
        'gas': float(gas_density)
    }
    if storage_kind in chemical_dencity.keys():
        return chemical_dencity[storage_kind]



def get_chemical_thickness(embank_height):
    """
    Получение толщины слоя жидкости
    embank_height - высота поддона или обваловки
    Толщина h слоя жидкости для АХОВ, разлившихся свободно на подстилающей поверхности,
    принимается равной 0,05 м по всей площади разлива; для АХОВ, разлившихся в поддон или обваловку,
    определяется следующим образом:
    а) при разливах из емкостей, имеющих самостоятельный поддон (обваловку):
    h = H - 0,2,
    где H - высота поддона (обваловки), м;
    б)  для емкостей имеющих общий поддон (обвалование) на группу:
    h = Q0 / F * d
    Q0 - колличетво выброшенного вещества при аварии (т)
    F - реальная площадь разлива в поддон (квадр. метр)
    d - плотность АХОВ (т/м3)
    :param embank_height:
    :return: float
    """
    return 0.05 if embank_height == 0 else (embank_height - 0.2)


def get_evaporation_duration(chemical_thickness, density, k2, k4, k7_2):
    """
    Время испарения АХОВ с площади разлива (в часах)
    T = h * d / k2 * k4 * k7
    где: h/layer_thickness – толщина слоя АХОВ, м ;
    d/density – удельная масса АХОВ, т/м3 (табл. П-2);
    k2, k4, k7 – коэффициенты.
    :param chemical_thickness: float
    :param density: float
    :param k2: float
    :param k4: float
    :param k7: float
    :return: float (часов)
    """
    EvaporationTime = namedtuple('EvaporationTime', ['in_hours', 'timedelta'])
    in_hours = round((chemical_thickness * density / (k2 * k4 * k7_2)), 5)
    minutes = round(round(math.modf(in_hours)[0], 2) * 60, 2)
    hours = math.modf(in_hours)[1]
    print('hours %s' % hours)
    print('minutes  %s' % minutes)
    # return timedelta(hours=hours, minutes=minutes)
    return EvaporationTime(
        in_hours=round(in_hours, 2),
        timedelta=timedelta(hours=hours, minutes=minutes)
    )


def get_angular_size(wind_speed):
    '''
    :param wind_speed: float (м/с)
    :return: int Значение углового размера зоны заражения (град)
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



def get_possible_contamination_area(contamination_depth, angular_size):
    '''
    :param contamination_depth:
    :param wind_speed:
    :return: площадь зоны возможного заражения АХОВ при времени испарения не более 4 часов (квадр. км)
    '''
    fi = angular_size
    contamination_area = (math.pi * contamination_depth ** 2 * fi) / 360
    return contamination_area


def get_actual_contamination_area(contamination_depth, dovsoa, after_crash_time):
    '''
    :param contamination_depth: (км)
    :param dovsoa: ( in 'ин', 'из', 'к')
    :param after_crash_time: (ч)
    :return: площадь зоны фактического заражения АХОВ  (квадр. км)
    '''
    k8_list = {'ин': 0.081, 'из': 0.133, 'к': 0.235}
    actual_contamination_area = k8_list[dovsoa] * contamination_depth ** 2 * after_crash_time ** 0.2
    return actual_contamination_area