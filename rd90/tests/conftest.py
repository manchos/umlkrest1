from django.conf import settings
from django.core.management import call_command
import pytest

def pytest_configure():
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'geobjects',
            'hazard_substance',
            'rd90',
            'weather',
        ],
        DATABASES={

            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'umlkrest',
                'USER': 'gisadmin',
                'PASSWORD': '171717',
                'HOST': 'localhost',
                'PORT': '',
            }
        }
    )


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'hazardous_chemicals_dump.json')