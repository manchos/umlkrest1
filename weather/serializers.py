from rest_framework import serializers
from weather.models import Weather
from collections import OrderedDict


class ChoicesSerializerField(serializers.SerializerMethodField):
    """
    A read-only field that return the representation of a model field with choices.
    """

    def to_representation(self, value):
        # sample: 'get_XXXX_display'
        method_name = 'get_{field_name}_display'.format(field_name=self.field_name)
        # retrieve instance method
        method = getattr(value, method_name)
        # finally use instance method to return result of get_XXXX_display()
        return method()



class WeatherSerializer(serializers.ModelSerializer):
    # wind_direction = ChoicesSerializerField()
    class Meta:
        model = Weather
        fields = (
            'id',
            'city_name',
            'dtime',
            'time_of_day',
            'wind_speed',
            'wind_direction',
            'air_t',
            'atmospheric_pressure',
            'is_snow',
            'cloud_score',
            'dovsoa',
        )