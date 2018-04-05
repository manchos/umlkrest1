from django.db import models
from django.contrib.gis.db import models as gismodels
# from django.contrib.gis.geos import Pod
from django.contrib.gis.geos import GEOSGeometry
import geocoder
from hazard_substance.models import HazardousChemical
from .utils import get_moscow_district, get_district_short_name, set_request_cache, ChoiceEnum
from model_utils import Choices


# Create your models here.
class Flood(gismodels.Model):
    ob = models.IntegerField()
    river = models.CharField(max_length=100)
    riv_sys = models.CharField(max_length=100)
    riv_in_sys = models.FloatField()
    geom = gismodels.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.river


class ObjectType(models.Model):
    name = models.CharField(max_length=200)
    descr = models.TextField(max_length=500, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'objects_types'
        verbose_name = 'Тип объектов'
        verbose_name_plural = 'Типы объектов'


class Object(gismodels.Model):
    name = models.CharField(max_length=300, verbose_name='Объект')
    address = models.CharField(max_length=400, verbose_name='Адрес')
    location = gismodels.PointField(
        srid=4326,
        null=True,
        blank=True,
        verbose_name='Координаты (вычисляются)')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    contacts = models.TextField(max_length=600, blank=True, default='', verbose_name='Контактные данные')

    DISTRICT_CHOICES = (
        ('ЦАО', 'ЦАО'),
        ('САО', 'САО'),
        ('СВАО', 'СВАО'),
        ('ВАО', 'ВАО'),
        ('ЮВАО', 'ЮВАО'),
        ('ЮАО', 'ЮАО'),
        ('ЮЗАО', 'ЮЗАО'),
        ('ЗАО', 'ЗАО'),
        ('СЗАО', 'СЗАО'),
        ('ЗелАО', 'ЗелАО'),
        ('НАО', 'НАО'),
        ('ТАО', 'ТАО'),
        ('', 'вычисляется')
    )
    
    # class Districts(ChoiceEnum):
    #     CAO = 'ЦАО'
    #     SAO = 'САО'
    #     SVAO = 'СВАО'
    #     VAO = 'ВАО'
    #     YVAO = 'ЮВАО'
    #     YAO = 'ЮАО'
    #     YZAO = 'ЮЗАО'
    #     ZAO = 'ЗАО'
    #     SZAO = 'CЗАО'
    #     ZelAO = 'ЗелАО'
    #     NAO = 'НАО'
    #     TAO = 'ТАО'
    #     NO = 'вычисляется'


    # DISTRICT_CHOICES = (
    #     (CAO, 'ЦАО'),
    #     (SAO, 'САО'),
    #     (SVAO, 'СВАО'),
    #     (VAO, 'ВАО'),
    #     (YVAO, 'ЮВАО'),
    #     (YAO, 'ЮАО'),
    #     (YZAO, 'ЮЗАО'),
    #     (ZAO, 'ЗАО'),
    #     (SZAO, 'CЗАО'),
    #     (ZELAO, 'ЗелАО'),
    #     (NAO, 'НАО'),
    #     (TAO, 'ТАО'),
    #     ('', 'вычисляется'),
    # )

    # DISTRICTS = Choices('ЦАО', 'САО','СВАО','ВАО','ЮВАО','ЮАО','ЮЗАО','ЗАО','CЗАО','ЗелАО','НАО','ТАО','вычисляется')

    district = models.CharField(
        max_length=15,
        blank=True,
        # choices=Districts.choices(),
        choices=DISTRICT_CHOICES,
        verbose_name='Округ',
        # default=Districts.NO,
        default='',
    )

    object_type = models.ForeignKey(
        ObjectType,
        on_delete=models.CASCADE,
        verbose_name='Тип объекта',
    )


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'objects'
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class FeatureType(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    descr = models.TextField(max_length=500, blank=True, verbose_name='описание')
    unit_measure = models.CharField(max_length=50, blank=True, verbose_name='единица измерения')
    ident_name = models.CharField(max_length=50, blank=True, verbose_name='идентификационное имя')
    object_type = models.ForeignKey(
        ObjectType,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'objects_types_features'
        verbose_name = 'Свойство типа объекта'
        verbose_name_plural = 'Свойства типов объектов'


class Feature(models.Model):
    feature_type = models.ForeignKey(
        FeatureType,
        on_delete=models.CASCADE,
        verbose_name='свойство типа'
    )
    object = models.ForeignKey(
        Object,
        on_delete=models.CASCADE,
        related_name='features',
    )
    value = models.CharField(max_length=200, verbose_name='значение')

    def __str__(self):
        return '{}: {}: {}'.format(self.object, self.feature_type, self.value)

    class Meta:
        db_table = 'objects_features'
        verbose_name = 'Свойство объекта'
        verbose_name_plural = 'Свойства объекта'


class SubstanceAmount(models.Model):

    hazard_substance = models.ForeignKey(
        HazardousChemical,
        on_delete=models.CASCADE,
        verbose_name='Опасное вещество на объекте',
    )

    object = models.ForeignKey(
        Object,
        on_delete=models.CASCADE,
    )

    FULL = 'full'
    ONE_TANK = 'one_tank'

    AMOUNT_FOR_CHOICES = (
        (FULL, 'всех емкостей'),
        (ONE_TANK, 'одной емкости'),
    )

    amount_for = models.CharField(
        max_length=20,
        blank=True,
        choices=AMOUNT_FOR_CHOICES,
        verbose_name='Количество для',
        default=FULL,
    )

    substance_amount = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name='Количество вещества (т)',
        default=0,
    )

    # full_substance_amount = models.IntegerField(
    #     blank=True,
    #     verbose_name='Общее количество вещества (т)',
    #     default=0,
    # )
    #
    # tank_substance_amount = models.IntegerField(
    #     blank=True,
    #     verbose_name='Количество вещества в 1 емкости (т)',
    #     default=0,
    # )

    STORAGE_CHOICES = (
        ('liquid', 'жидкость'),
        ('gas_no_pressure', 'газ'),
        ('gas_under_pressure', 'газ под давлением')
    )

    hc_storage = models.CharField(
        max_length=20,
        choices=STORAGE_CHOICES,
        default='liquid',
        verbose_name='Хранение АХОВ',
    )

    embank_height = models.FloatField(
        blank=True,
        verbose_name='Dысота поддона или обваловки (м)',
        default=0,
    )



    def __str__(self):
        return '{}: {}: количество: {} т. для {}, Способ хранения: {}'.format(
            self.object, self.hazard_substance, self.substance_amount,  self.get_amount_for_display(), self.get_hc_storage_display())

    class Meta:
        db_table = 'substance_amounts'
        verbose_name = 'Количество вещества'
        verbose_name_plural = 'Количество вещества'


from django.db.models.signals import pre_save
from django.dispatch import receiver


set_request_cache()



@receiver(pre_save, sender=Object)
def geocoding_from_address(sender, instance, **kwargs):
    if instance.address:
        g = geocoder.yandex(instance.address)
        latitude = g.latlng[0]
        longitude = g.latlng[1]
        pnt = 'POINT({} {})'.format(str(longitude), str(latitude))
        # instance.location = Point(str(longitude), str(latitude), srid=4326)
        instance.location = GEOSGeometry(pnt, srid=4326)

@receiver(pre_save, sender=Object)
def get_moscow_district_from_address(sender, instance, **kwargs):
    if instance.address:
        g = geocoder.yandex(instance.address)
        latitude = str(g.latlng[0])
        longitude = str(g.latlng[1])
        district_full_name = get_moscow_district(longitude, latitude)
        print(district_full_name)
        instance.district = get_district_short_name(district_full_name)
        print(instance.district)
    # def perform_create(self, serializer):
    #     address = serializer.initial_data['address']
    #     g = geocoder.yandex(address)
    #     latitude = g.latlng[0]
    #     longitude = g.latlng[1]
    #     pnt = 'POINT({} {})'.format(str(longitude), str(latitude))
    #     serializer.save(location=pnt)