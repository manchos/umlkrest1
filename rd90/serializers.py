from rest_framework import serializers
from rd90.models import Rd90Calc
from weather.serializers import WeatherSerializer
# from django.contrib.auth.models import User
from geobjects.serializers import ObjectSerializer
from profiles.models import CustomUser


class Rd90CalcSerializer(serializers.ModelSerializer):
    weather = WeatherSerializer()
    chem_danger_object = ObjectSerializer()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Rd90Calc
        fields = (
            'id',
            'owner',
            'get_chemicals',
            'crash_dtime',
            'after_crash_time',
            'chem_danger_object',
            'weather',
            'evaporation_duration',
            'full_contamination_depth',
            'angular_size',
            'possible_contamination_area',
            'actual_contamination_area',
            'json_calculation',
        )





class UserSerializer(serializers.ModelSerializer):
    rd90calcs = serializers.PrimaryKeyRelatedField(many=True, queryset=Rd90Calc.objects.all())

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'rd90calcs')

