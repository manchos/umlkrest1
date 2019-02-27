from django.contrib import admin

# Register your models here.
from .models import WaterBody, IceCheckPost, IceThickness
from regions.models import Region
from leaflet.admin import LeafletGeoAdmin
from profiles.models import CustomUser
import logging
from crum import get_current_user



logging.debug('Debug Message')


class IceCheckPostInline(admin.StackedInline):
    model = IceCheckPost


class WaterBodyAdmin(admin.ModelAdmin):

    # list_editable = ('is_active',)
    #prepopulated_fields = {"slug_name": ("short_name",)}
    # Specify name of sortable property
    # sortable = 'order'
    # kwargs['initial'] = request.user.id
    list_select_related = ('region',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name == 'region' and
                request.user.is_region):
            kwargs['initial'] = request.user.region
            kwargs['queryset'] = Region.objects.filter(name=request.user.region)
        return (
            super(WaterBodyAdmin, self)
            .formfield_for_foreignkey(db_field, request, **kwargs)
        )

    list_display = ('water_type', 'name', 'region', 'description')
    list_display_links = ('water_type', 'name', )


admin.site.register(WaterBody, WaterBodyAdmin)


class IceCheckPostAdmin(LeafletGeoAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (55.754646, 37.621463),
        'DEFAULT_ZOOM': 10,
    }
    fields = ('water_body', 'name', 'location')
    list_select_related = ('water_body',)

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'water_body':
    #         obj_id = int(request.path.split('/')[4])
    #         obj = IceCheckPost.objects.get(pk=obj_id)
    #         self.set_map_center(obj)
    #     return super(IceCheckPostAdmin, self).formfield_for_foreignkey(
    #         db_field, request, **kwargs
    #     )

    def get_fields(self, request, obj):
        map_center = ''
        if obj:
            map_center = obj.water_body.region.map_center
        else:
            user = get_current_user()
            if user.is_region:
                map_center = user.region.map_center
        self.set_map_center(map_center)
        return list(IceCheckPostAdmin.fields)

    def set_map_center(self, map_center):
        # logging.error(map_center)
        if map_center:
            self.settings_overrides['DEFAULT_CENTER'] = (
                map_center.y,
                map_center.x,
            )
            self.settings_overrides['DEFAULT_ZOOM'] = 8


    list_display = ('water_body', 'name', 'get_region')

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


admin.site.register(IceCheckPost, IceCheckPostAdmin)

                    # , IceCheckPostAdmin)


class IceThicknessAdmin(admin.ModelAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (55.754646, 37.621463),
        'DEFAULT_ZOOM': 8,
    }
    list_display = ('ice_check_post', 'check_date', 'thick_val_min',
                    'thick_val_max', 'thick_val_average', 'description', 'modified')

    list_editable = ('ice_check_post', 'check_date', 'thick_val_min',
                    'thick_val_max', 'thick_val_average', 'description')
    list_display_links = None

    list_select_related = ('ice_check_post',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'ice_check_post' and request.user.is_region:
            kwargs['queryset'] = IceCheckPost.objects.filter(
                water_body__region_id=request.user.region_id
            )
        return super(IceThicknessAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


admin.site.register(IceThickness, IceThicknessAdmin)
# admin.site.register(IceThickness)