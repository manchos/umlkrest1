import requests
from bs4 import BeautifulSoup


def get_html_meteo(url='http://old.meteoinfo.ru/pogoda/russia/moscow-area/moscow'):
    headers = {'User-agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'}
    try:
        return requests.get(url, headers=headers).text
    except (ConnectionError, requests.exceptions.ConnectionError) as exc:
        print(exc)
        return None


def determine_clouding_text(cloud_score):
    '''
        Облачность выдается в баллах по 10-балльной шкале,
        0 баллов = ясно,
        1-3 балла = малооблачно,
        4-7 баллов - облачно,
        7-10 баллов - пасмурно.
    :param cloud_score:
    :return: clouding_text
    '''
    clouding_dict = {
        'ясно': {0},
        'малооблачно': range(1, 4),
        'облачно': range(4, 8),
        'пасмурно': range(7, 11),
    }
    for clouding_text, _range in clouding_dict.items():
        if cloud_score in _range:
            return clouding_text


def is_cloudiness(cloud_score):
    if cloud_score is None:
        return None

    if cloud_score >= 4:
        return True
    else:
        return False


def get_meteo_info_dict(html):
    bs = BeautifulSoup(html, 'html.parser')
    meteo_info = {}

    for item in bs.find_all('th', 'pogodacell2'):

        value = item.next_sibling.next_sibling.text
        # print(" %s : %s" % (item.text.lower(), value))
        if item.text.lower().find('давлени') > 0:
            meteo_info['pressure'] = value
        if item.text.lower().find('емпература') > 0:
            meteo_info['t'] = value
        if item.text.lower().find('влажност') > 0:
            meteo_info['humidity'] = value
        if item.text.find('аправлени', 0) > 0:
            meteo_info['wind_direction'] = value
        if item.text.lower().find('корост') > 0:
            meteo_info['wind_speed'] = value
        if item.text.lower().find('облачност') > 0:
            meteo_info['clouding'] = value
        if item.text.lower().find('видимост') > 0:
            meteo_info['visibility'] = value

    return meteo_info

    # print(item.next_sibling.next_sibling.text)

#
# night, clear|partly cloudy, overcast

if __name__ == '__main__':
    html = get_html_meteo()
    print('{}'.format(get_meteo_info_dict(html)))
