# from suit.admin import SortableModelAdmin
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Region
from leaflet.admin import LeafletGeoAdmin

class RegionAdmin(MPTTModelAdmin, LeafletGeoAdmin):
    mptt_level_indent = 20
    # list_display = ('name', 'slug', 'is_active', 'order')
    # list_editable = ('is_active',)
    prepopulated_fields = {"slug_name": ("short_name",)}
    # Specify name of sortable property
    # sortable = 'order'

admin.site.register(Region, RegionAdmin)

# admin.site.register(Region, MPTTModelAdmin)

# Register your models here.
