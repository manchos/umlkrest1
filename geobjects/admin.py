from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
# Register your models here.


from .models import Object, ObjectType, FeatureType, Feature, SubstanceInfo


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1


class SubstanceAmountInline(admin.TabularInline):
    model = SubstanceInfo
    extra = 1

# admin.site.register(Object)
admin.site.register(ObjectType)
admin.site.register(FeatureType)
admin.site.register(Feature)
admin.site.register(SubstanceInfo)


class ObjectAdmin(LeafletGeoAdmin):
    list_display = ('name', 'district', 'address', 'object_type', 'location')
    inlines = [SubstanceAmountInline, FeatureInline]

admin.site.register(Object, ObjectAdmin)


class FeatureAdmin(LeafletGeoAdmin):
    list_display = ('name', 'district', 'address', 'object_type', 'location')
    inlines = [FeatureInline]


# class FloodAdmin(LeafletGeoAdmin):
#     list_display = ('river', 'riv_sys', 'riv_in_sys')
#     list_per_page = 10
#
# admin.site.register(Flood, FloodAdmin)