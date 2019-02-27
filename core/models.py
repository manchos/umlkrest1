from django.db import models
from crum import get_current_user
from profiles.models import CustomUser
from django.utils.functional import cached_property

# Create your models here.


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(CustomUser, blank=True, null=True,
                                   default=None,
                                   related_name='ice_thickness',
                                   on_delete=models.SET_NULL,)
    modified_by = models.ForeignKey(CustomUser, blank=True, null=True,
                                    default=None,
                                    related_name='+',
                                    on_delete=models.SET_NULL,)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class RegionManager(models.Manager):

    @cached_property
    def get_region(self):
        user = get_current_user()
        if user.is_region():
            return user.region
        else:
            return None


# class Regionable(models.Model):
#     slug = models.SlugField()
#
#     class Meta:
#         abstract = True
