from astral import Astral
from datetime import datetime, date, time, timedelta, tzinfo

from collections import namedtuple
import datetime

import pytz

utc=pytz.UTC

from django.utils import timezone

# Task.__new__.__defaults__ = (None, None, False, None)


# нахождение времени суток
def get_time_of_day(_datetime, city_name='Moscow'):
    a = Astral()
    print('время аварии %s' % _datetime)
    # a.solar_depression = 'civil'
    city = a[city_name]
    _datetime = pytz.timezone(city.timezone).localize(_datetime)


    sun = city.sun(date=_datetime.date(), local=True)
    timezone = city.timezone
    print('Timezone: %s' % timezone)

    # sunrise = sun['sunrise'].replace(tzinfo=None)
    sunrise = sun['sunrise']
    print('sunrize {}'.format(sunrise))

    # start_earth_day = datetime.combine(_datetime.date(), time(0, 0))
    start_earth_day = _datetime.replace(hour=0, minute=0)

    # print('start_earth_day %s' % start_earth_day)
    print('start_earth_day %s' % start_earth_day)

    # end_earth_day = datetime.combine(_datetime.date(), time(23, 59))
    end_earth_day = _datetime.replace(hour=23, minute=59)

    # sunset = sun['sunset'].replace(tzinfo=None)
    sunset = sun['sunset']
    print('sunset {}'.format(sunset))

    # Под термином «утро» понимается период времени в течение 2 ч после восхода солнца
    # под термином «вечер» - в течение 2 ч после захода солнца
    # Период от восхода до захода солнца за вычетом двух утренних часов - день, а период от захода до восхода солнца за
    # вычетом двух вечерних часов - ночь.

    if _datetime > sunrise:
        # if (sunrise + timedelta(hours=2)).replace(tzinfo=None) < _datetime < sunset:
        if (sunrise + timedelta(hours=2)) < _datetime < sunset:

            return 'day'
        elif _datetime - sunrise <= timedelta(hours=2):
            print('_datetime : %s' % _datetime)
            print('sunrise %s' % sunrise)
            print('_datetime - sunrise %s' % (_datetime - sunrise))
            return 'morning'
        elif _datetime - sunset <= timedelta(hours=2):
            return 'evening'
        # elif (sunset + timedelta(hours=2)).replace(tzinfo=None) < _datetime <= end_earth_day:
        elif (sunset + timedelta(hours=2)) < _datetime <= end_earth_day:
            return 'night'
    elif _datetime >= start_earth_day:
        return 'night'


# Определение степени вертикальной устойчивости воздуха по прогнозу погоды
def get_dovsoa(time_of_day, wind_speed, cloudiness=False, snow=False):
    # cloudiness - облачность
    # snow - наличие снежного покрова

    Dovsoa = namedtuple('Dovsoa', ['wind_speed', 'snow', 'cloudiness', 'night', 'morning', 'day', 'evening'])
    
    if type(snow) != bool and type(cloudiness) != bool:
        return None
    if time_of_day not in {'morning', 'night', 'day', 'evening'}:
        return None

    wind_speed_r = float(wind_speed)
    if wind_speed_r < 2:
        wind_speed = 'V<2'
    elif 2 <= wind_speed_r <= 3.9:
        wind_speed = '2<=V<=3.9'
    elif wind_speed_r > 4:
        wind_speed = 'V>4'

    dovsoa_tuple = (
        Dovsoa('V<2', False, False, 'ин', 'из', 'к', 'ин'),
        Dovsoa('V<2', True, True, 'из', 'из', 'из', 'из'),
        Dovsoa('V<2', True, False, 'ин', 'ин', 'из', 'ин'),
        Dovsoa('V<2', False, True, 'из', 'из', 'из', 'из'),

        Dovsoa('2<=V<=3.9', False, False, 'ин', 'из', 'из', 'из'),
        Dovsoa('2<=V<=3.9', True, True, 'из', 'из', 'из', 'из'),
        Dovsoa('2<=V<=3.9', True, False, 'ин', 'ин', 'из', 'ин'),
        Dovsoa('2<=V<=3.9', False, True, 'из', 'из', 'из', 'из'),

        Dovsoa('V>4', False, False, 'из', 'из', 'из', 'из'),
        Dovsoa('V>4', True, True, 'из', 'из', 'из', 'из'),
        Dovsoa('V>4', True, False, 'из', 'из', 'из', 'из'),
        Dovsoa('V>4', False, True, 'из', 'из', 'из', 'из'),
    )
    dovsoa = [d.__getattribute__(time_of_day) for d in dovsoa_tuple
              if (d.wind_speed, d.snow, d.cloudiness) == (wind_speed, snow, cloudiness)][0]

    return dovsoa


def get_dovsoa_word(dovsoa):
    if not dovsoa:
        return ''
    print_list = {
        'к': 'конверсия',
        'из': 'изометрия',
        'ин': 'инверсия',
    }
    return print_list[dovsoa]


if __name__ == '__main__':
    # dovsoa = get_dovsoa(datetime.now(), 1, cloudiness=False, snow=False)
    # print('сейчас время суток: {}'.format(get_time_of_day(datetime.now())))
    # print('степени вертикальной устойчивости воздуха: {}'.format(dovsoa))

    my_datetime = datetime.datetime(year=2018, month=7, day=3, hour=4, minute=50, tzinfo=utc)
    time_of_day = get_time_of_day(my_datetime)


# if (sun['sunrise'] < T < sun['sunset']) and (light < threshold):


