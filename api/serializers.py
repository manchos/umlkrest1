from rest_framework import serializers
from rd90.models import Rd90Calc
from weather.models import Weather
from rest_framework.renderers import JSONRenderer



# class WeatherSerializer(serializers.ModelSerializer):
#     # dovsoa = Weather.get_dovsoa_display()
#
#     class Meta:
#         model = Weather
#         fields = ('dovsoa', 'air_t', 'wind_direction', 'wind_speed')


class Rd90CalcSerializer(serializers.ModelSerializer):

    # weather = WeatherSerializer(read_only=True)

    class Meta:
        model = Rd90Calc
        fields = ('id', 'crash_dtime', 'after_crash_time', 'weather',
                  'chem_danger_object', 'chemical', 'evaporation_duration',
                  'full_contamination_depth', 'angular_size', 'json_calculation')




