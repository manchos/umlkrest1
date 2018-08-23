from django.test import TestCase
import weather.dovsoa

import datetime


# Dovsoa('V<2', False, False, 'ин', 'из', 'к', 'ин'),
# Dovsoa('2<=V<=3.9', True, False, 'ин', 'ин', 'из', 'ин')
# Dovsoa('2<=V<=3.9', False, True, 'из', 'из', 'из', 'из'),

# Create your tests here.
def test_time_of_day_dovsoa(_datetime=datetime.datetime(year=2018, month=7, day=3, hour=6, minute=0)):
    time_of_day = weather.dovsoa.get_time_of_day(_datetime)
    dovsoa = weather.dovsoa.get_dovsoa(time_of_day=time_of_day, wind_speed=1, cloudiness=False, snow=False)
    assert 'day' == time_of_day
    assert 'к' == dovsoa

# Create your tests here.
def test_time_of_evening_dovsoa(_datetime=datetime.datetime(year=2018, month=7, day=3, hour=22, minute=0)):
    time_of_day = weather.dovsoa.get_time_of_day(_datetime)
    dovsoa = weather.dovsoa.get_dovsoa(time_of_day=time_of_day, wind_speed=3.8, cloudiness=True, snow=False)
    assert 'evening' == time_of_day
    assert 'из' == dovsoa
