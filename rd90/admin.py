from django.contrib import admin
from geobjects.models import Object, ObjectType, FeatureType, Feature, SubstanceInfo

# Register your models here.

from .models import Rd90Calc
from .models import Weather

# admin.site.register(Object)
# admin.site.register(Rd90Calc)

admin.site.register(Weather)

# chemicals_amount = property(Rd90Calc.chemicals_amount)

#
# class Rd90CalcAdmin(admin.ModelAdmin):
#     list_display = ('chem_danger_object', 'chemicals_amount')
#     # inlines = [SubstanceAmountInline, FeatureInline]


class Rd90CalcAdmin(admin.ModelAdmin):
    list_display = ('chem_danger_object', 'get_chemicals', 'weather')
    # list_display = ('chem_danger_object')
    readonly_fields = (
        'evaporation_duration',
        'full_contamination_depth',
        'angular_size',
        'possible_contamination_area',
        'actual_contamination_area',
        'json_calculation',
    )

    fieldsets = (
        (None, {
            'fields': (
                'crash_dtime',
                'after_crash_time',
                'weather',
            )
        }),
        # ('Погодные условия', {
        #     'fields': (
        #
        #         ('wind_speed', 'wind_direction', ),
        #         ('air_t', 'dovsoa')
        #
        #     ),
        # }),
        ('Объектовые данные', {
             'fields': (

                 ('chem_danger_object', 'chemical'),


             )
        }),
        ('Расчетные данные', {
            'fields': (

                ('evaporation_duration', 'full_contamination_depth',
                 'angular_size', 'possible_contamination_area',
                 'actual_contamination_area'),
                'json_calculation'

            )
        }),

        # ('Advanced options', {
        #     'classes': ('collapse',),
        #     'fields': ('registration_required', 'template_name'),
        # }),
    )

admin.site.register(Rd90Calc, Rd90CalcAdmin)