from django.contrib.gis.db import models


# Create your models here.

class ObjectType(models.Model):
    name = models.CharField(max_length=200)
    descr = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'objecttypes'
        verbose_name = 'Тип объектов'
        verbose_name_plural = 'Типы объектов'


class Object(models.Model):
    name = models.CharField(max_length=300, verbose_name='Объект')
    address = models.CharField(max_length=400, verbose_name='Адрес')
    location = models.PointField(srid=4326, null=True, blank=True, verbose_name='Координаты')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    contacts = models.CharField(max_length=600, verbose_name='Контактные данные')

    object_type = models.ForeignKey(
        ObjectType,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'objects'
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class FeatureType(models.Model):
    name = models.CharField(max_length=200)
    descr = models.CharField(max_length=500)
    unit_measure = models.CharField(max_length=50)
    object_type = models.ForeignKey(
        ObjectType,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'featuretypes'
        verbose_name = 'Свойство объекта'
        verbose_name_plural = 'Свойства объектов'


class Feature(models.Model):
    feature_type = models.ForeignKey(
        FeatureType,
        on_delete=models.CASCADE,
    )
    object_type = models.ForeignKey(
        ObjectType,
        on_delete=models.CASCADE,
    )
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.value