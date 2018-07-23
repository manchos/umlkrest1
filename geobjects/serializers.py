from rest_framework import serializers
from geobjects.models import Object


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



class ObjectSerializer(serializers.ModelSerializer):
    # wind_direction = ChoicesSerializerField()
    class Meta:
        model = Object
        fields = (
            'id',
            'name',
            'address',
            'location',
            # 'address',
            # 'location',
            # 'contacts',
            # 'district',
            # 'object_type',
            # 'k1',
            # 'k2',
            # 'k3',
            # 'k7_1',
            # 'k7_2',
        )