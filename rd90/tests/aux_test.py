import rd90.calc.aux as aux
import pytest
from datetime import datetime, date, timedelta
import sympy

from hazard_substance.models import HazardousChemical
from django.test import TestCase


@pytest.fixture(params=[
    (4, 2.0),
    (5, 2.34),
    (2, 1.33),
    (8.5, 3.505),
    (17.3, 5.68)
], ids=['', '', 'wind_speed = 2 m/s', '', 'wind_speed = 17 m/s'])
def k4_param(request):
    return request.param

def test_get_k4(k4_param):
    wind_speed_input, expected_k4 = k4_param
    assert expected_k4 == aux.get_k4(wind_speed=wind_speed_input)


@pytest.fixture(params=[
    ((20, 1, '[[0,0.3,0.6,1,1.4],[0.9,1,1,1,1]]', 'gas_no_pressure'), 1.0),
    ((20, 2, '[[0,0.3,0.6,1,1.4],[0.9,1,1,1,1]]', 'gas_no_pressure'), 1.0),
    ((-25, 1, '[[0.3,0.5,0.8,1,1.2],[1,1,1,1,1]]', 'gas_no_pressure'), 0.45),
    ((0, 1, '[[0.0, 0.3, 0.6, 1.0, 1.4],[0.9, 1.0, 1.0, 1.0, 1.0]]', 'liquid'), 0.6),
    ((0, 2, '[[0.0, 0.3, 0.6, 1.0, 1.4],[0.9, 1.0, 1.0, 1.0, 1.0]]', 'liquid'), 1.0),
], ids=['', '', '', 'Cl cloud-I', 'Cl cloud-II'])
def k7_param(request):
    return request.param

def test_get_k7(k7_param):
    params, expected_k7 = k7_param
    air_t, cloud_number, k7, hc_storage = params
    assert expected_k7 == aux.get_k7(
        air_t=air_t,
        cloud_number=cloud_number,
        k7_json=k7,
        storage_kind=hc_storage
    )
    # assert expected_k7 == get_k7(*params)


@pytest.fixture(params=[
    (timedelta(hours=0.5), timedelta(hours=1.5), 1),
    (timedelta(hours=1), timedelta(hours=1.5), 1.0),
    (timedelta(hours=2.5), timedelta(hours=2), 1.7411)
], ids=['for < 1 hour', '', ''])
def k6_param(request):
    return request.param

def test_get_k6(k6_param):
    after_crash_time, evaporation_duration, expected_k6 = k6_param
    assert expected_k6 == aux.get_k6(after_crash_time, evaporation_duration)
    # assert expected_k7 == get_k7(*params)

# def get_contamination_depth(equivalent_amount, wind_speed):

@pytest.fixture(params=[
    ((0.5, 0.18, 0.052, 2.34, 1), 0.74),
    ((1.8, 1.553, 0.052, 1.33, 1), 40.42),
], ids=['', ''])
def evaporation_duration_param(request):
    return request.param

def test_get_evaporation_duration(evaporation_duration_param):
    params, expected_evaporation_duration = evaporation_duration_param
    chemical_thickness, density, k2, k4, k7_2 = params
    assert expected_evaporation_duration == aux.get_evaporation_duration(
        chemical_thickness=chemical_thickness,
        density=density,
        k2=k2, k4=k4, k7_2=k7_2
    ).in_hours


# aux.get_evaporation_duration(chemical_thickness=)

# @pytest.fixture(params=[
#     ((20, 1, '[[0,0.3,0.6,1,1.4],[0.9,1,1,1,1]]', 'gas_no_pressure'), 1.0),
#     ((20, 2, '[[0,0.3,0.6,1,1.4],[0.9,1,1,1,1]]', 'gas_no_pressure'), 1.0),
#     ((-25, 1, '[[0.3,0.5,0.8,1,1.2],[1,1,1,1,1]]', 'gas_no_pressure'), 0.45)
# ], ids=['', '', ''])
# def evaporation_duration_param(request):
#     return request.param
#
# def get_evaporation_duration(evaporation_duration_param):
#     params, expected_evaporation_duration = evaporation_dur
#         density=density,
#         k2=k2,ation_param
#     layer_thickness, density, k2, k4, k7 = params
#     assert expected_evaporation_duration == aux.get_evaporation_duration(
#         layer_thickness=layer_thickness,
#         k4=k4,
#         k7=k7,
#     )

# @pytest.fixture(scope='session')
# def django_db_modify_db_settings():
#     pass

@pytest.mark.django_db(transaction=False)
def test_my_user():
    # HazardousChemical.objects.create(id=29)
    chlor = HazardousChemical.objects.get(id=30)
        # objects.get(id=30)
    assert chlor.k7 == '[[0.0, 0.3, 0.6, 1.0, 1.4],[0.9, 1.0, 1.0, 1.0, 1.0]]'
    # assert chlor.name == 'Хлорр'

# class AnimalTestCase(TestCase):


# print(get_k7(air_t=5, cloud_number=1, k7_json='[[0.3,0.5,0.8,1,1.2],[1,1,1,1,1]]', hc_storage='gas_no_pressure'))