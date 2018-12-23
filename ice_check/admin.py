from django.contrib import admin

# Register your models here.

from .models import WaterBody
from .models import IceCheckPost
from regions.models import Region
from .models import IceThickness
from profiles.models import CustomUser



class WaterBodyAdmin(admin.ModelAdmin):

    # list_editable = ('is_active',)
    #prepopulated_fields = {"slug_name": ("short_name",)}
    # Specify name of sortable property
    # sortable = 'order'
    # kwargs['initial'] = request.user.id


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'region' and request.user.groups.filter(name='федеральный округ').exists():
            kwargs['initial'] = request.user.region
            kwargs['queryset'] = Region.objects.filter(name=request.user.region)
        return super(WaterBodyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_region(self, request, ):
    #     if
    list_display = ('water_type', 'name', 'region', 'description')
    list_display_links = ('water_type', 'name', )

admin.site.register(WaterBody, WaterBodyAdmin)

admin.site.register(IceCheckPost)
admin.site.register(IceThickness)