from astral import Astral
from datetime import datetime, date, time, timedelta, tzinfo


# нахождение времени суток
def get_time_of_day(dt, city_name='Moscow'):
    a = Astral()
    print(dt)
    # a.solar_depression = 'civil'
    city = a[city_name]
    sun = city.sun(date=dt.date(), local=True)
    timezone = city.timezone
    print('Timezone: %s' % timezone)

    # sunrise = sun['sunrise'].replace(tzinfo=None)
    sunrise = sun['sunrise']
    print('sunrize {}'.format(sunrise))


    start_earth_day = datetime.combine(dt.date(), time(0, 0))
    end_earth_day = datetime.combine(dt.date(), time(23, 59))
    # sunset = sun['sunset'].replace(tzinfo=None)
    sunset = sun['sunset']

    if dt > sunrise:
        # if (sunrise + timedelta(hours=2)).replace(tzinfo=None) < dt < sunset:
        if (sunrise + timedelta(hours=2)) < dt < sunset:

            return 'day'
        elif dt - sunrise <= timedelta(hours=2):
            print('dt : %s' % dt)
            print('sunrise %s' % sunrise)
            print('dt - sunrise %s' % (dt - sunrise))
            return 'morning'
        elif dt - sunset <= timedelta(hours=2):
            return 'evening'
        # elif (sunset + timedelta(hours=2)).replace(tzinfo=None) < dt <= end_earth_day:
        elif (sunset + timedelta(hours=2)) < dt <= end_earth_day:
            return 'night'
    elif dt >= start_earth_day:
        return 'night'


# Определение степени вертикальной устойчивости воздуха по прогнозу погоды
def get_dovsoa(time_of_day, wind_speed, city_name='Moscow', cloudiness=False, snow=False):
    # cloudiness - облачность
    # snow - наличие снежного покрова

    if type(snow) != bool and type(cloudiness) != bool:
        return None
    if time_of_day not in ['morning', 'night', 'day', 'evening']:
        return None

    wind_speed_r = float(wind_speed)
    if wind_speed_r < 2:
        wind_speed = 'V<2'
    elif 2 <= wind_speed_r <= 3.9:
        wind_speed = '2<=V<=3.9'
    elif wind_speed_r > 4:
        wind_speed = 'V>4'

    dovsoa_list = [
        {'wind_speed': 'V<2', 'snow': False, 'cloudiness': False,
         'night':'ин', 'morning': 'из', 'day': 'к', 'evening':'ин'},
        {'wind_speed': 'V<2', 'snow': True, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': 'V<2', 'snow': True, 'cloudiness': False,
         'night': 'ин', 'morning': 'ин', 'day': 'из', 'evening': 'ин'},
        {'wind_speed': 'V<2', 'snow': False, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},

        {'wind_speed': '2<=V<=3.9', 'snow': False, 'cloudiness': False,
         'night':'ин', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': '2<=V<=3.9', 'snow': True, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': '2<=V<=3.9', 'snow': True, 'cloudiness': False,
         'night': 'ин', 'morning': 'ин', 'day': 'из', 'evening': 'ин'},
        {'wind_speed': '2<=V<=3.9', 'snow': False, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},

        {'wind_speed': 'V>4', 'snow': False, 'cloudiness':False,
         'night':'из', 'morning': 'из', 'day': 'из', 'evening':'из'},
        {'wind_speed': 'V>4', 'snow': True, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': 'V>4', 'snow': True, 'cloudiness': False,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
        {'wind_speed': 'V>4', 'snow': False, 'cloudiness': True,
         'night': 'из', 'morning': 'из', 'day': 'из', 'evening': 'из'},
     ]
    dovsoa = [x[time_of_day] for x in dovsoa_list if x['snow'] == snow and
            x['wind_speed'] == wind_speed and x['cloudiness'] == cloudiness][0]

    return dovsoa


def get_dovsoa_word(dovsoa):
    print_list = {
        'к': 'конверсия',
        'из': 'изометрия',
        'ин': 'инверсия',
    }
    return print_list[dovsoa]





if __name__ == '__main__':
    dovsoa = get_dovsoa(datetime.now(), 1, cloudiness=False, snow=False)
    print('сейчас время суток: {}'.format(get_time_of_day(datetime.now())))
    print('степени вертикальной устойчивости воздуха: {}'.format(dovsoa))

# Под термином «утро» понимается период времени в течение 2 ч после восхода солнца
# под термином «вечер» - в течение 2 ч после захода солнца
# Период от восхода до захода солнца за вычетом двух утренних часов - день, а период от захода до восхода солнца за
# вычетом двух вечерних часов - ночь.

# if (sun['sunrise'] < T < sun['sunset']) and (light < threshold):
