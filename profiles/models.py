from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from regions.models import Region
# from django.contrib.auth.models import Group, User
# from django.contrib import admin

# AUTH_USER_MODEL = 'profiles.CustomUser'

# admin.site.unregister(User)


class CustomUser(AbstractUser):
    # add additional fields in here
    mchs_phone_numb = models.CharField(max_length=100, verbose_name="тел. номер МЧС")
    sity_phone_numb = models.CharField(max_length=100, blank=True, null=True,
                                       verbose_name="тел. номер город. (с кодом)")
    phone_comment = models.TextField(blank=True, null=True, verbose_name="Комментарии к контактам")
    last_updated = models.DateTimeField(auto_now_add=True)
    # models.ForeignKey(Region, default=1, on_delete=models.SET_DEFAULT)

    region = models.ForeignKey(
        Region,
        related_name='users',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Регион"
    )
