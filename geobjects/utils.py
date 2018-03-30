import requests
import logging
import re
from enum import Enum
import requests_cache
import os

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


def get_page(url, session=None, verify=False):
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br'}
    try:
        if session is not None:
            # return browser
            return session.get(url, headers=headers, verify=verify)
        else:
            return requests.get(url, headers=headers, verify=verify)
    except (ConnectionError, requests.exceptions.ConnectionError) as exc:
        logging.error(exc)
        return None


def get_moscow_district(longitude, latitude, session=None):
    district_url = 'https://geocode-maps.yandex.ru/1.x/?geocode={},{}&kind=district&results=5&format=json' \
        .format(longitude, latitude)
    response = get_page(district_url, session, verify=False)
    # print(response.json()['response']['GeoObjectCollection']['featureMember'][1]['GeoObject']['name'])
    return (response.json()['response']['GeoObjectCollection']
            ['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']
            ['AddressDetails']['Country']['AdministrativeArea']['Locality']['DependentLocality']
            ['DependentLocalityName'])


def get_district_short_name(district_full_name): #'юго-восточный административный округ'
    district = district_full_name.strip()
    if 'Зел' in district:
        return 'ЗелАО'
    elif '-' in district:
        re_ = re.findall('^([а-яА-Я]+)[ ]?[-]{1}[ ]?([а-яА-Я]+)', district)[0]
    else:
        re_ = re.findall('^([а-яА-Я]+)[ ]+', district)

    return ''.join([a[:1].upper() for a in re_]) + 'АО' #ЮВАО

def set_request_cache():
    if not os.path.exists('_cache'):
        os.mkdir('_cache')
    requests_cache.install_cache('_cache/page_cache', backend='sqlite',
                                 expire_after=10800)