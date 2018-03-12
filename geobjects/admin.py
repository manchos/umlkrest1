from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
# Register your models here.


from .models import Object, ObjectType, FeatureType, Feature

# admin.site.register(Object)
admin.site.register(ObjectType)
admin.site.register(FeatureType)
admin.site.register(Feature)


class ObjectAdmin(LeafletGeoAdmin):
    list_display = ('name', 'address', 'location')

admin.site.register(Object, ObjectAdmin)
