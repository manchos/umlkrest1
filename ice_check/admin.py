from django.contrib import admin

# Register your models here.

from .models import WaterBody
from .models import IceCheckPost
from regions.models import Region
from .models import IceThickness
from leaflet.admin import LeafletGeoAdmin
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


# class IceCheckPostAdmin(admin.ModelAdmin):
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'water_body' and request.user.groups.filter(
    #             name='федеральный округ'
    #     ).exists():
    #         kwargs['queryset'] = WaterBody.objects.filter(
    #             region=request.user.region
    #         )
    #     return super(IceCheckPostAdmin, self).formfield_for_foreignkey(
    #         db_field, request, **kwargs
    #     )



admin.site.register(IceCheckPost, LeafletGeoAdmin)
                    # , IceCheckPostAdmin)


class IceThicknessAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'ice_check_post' and request.user.groups.filter(
                name='федеральный округ'
        ).exists():
            kwargs['queryset'] = IceCheckPost.objects.filter(
                water_body__region=request.user.region
            )
        return super(IceThicknessAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(IceThickness, IceThicknessAdmin)
# admin.site.register(IceThickness)