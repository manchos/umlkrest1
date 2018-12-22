from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser



class CustomUserAdmin(UserAdmin):


    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Персональная информация'), {
            'fields': (
                'first_name',
                'last_name',
                'region',
                'email',
                'mchs_phone_numb',
                'sity_phone_numb',
            )
        }),
        (('Разрешения'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'region', 'mchs_phone_numb', 'sity_phone_numb']


admin.site.register(CustomUser, CustomUserAdmin)
