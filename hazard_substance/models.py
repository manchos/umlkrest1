from django.db import models

# Create your models here.

class HazardousChemical(models.Model):
    name = models.CharField(max_length=255)
    form = models.CharField(null=True,max_length=255)
    gas_density = models.FloatField(null=True, blank=True)
    liquid_density = models.FloatField(null=True, blank=True)
    boiling_t = models.FloatField(null=True, blank=True)
    toxodeth = models.FloatField(null=True, blank=True)
    k1 = models.FloatField(null=True, blank=True)
    k2 = models.FloatField(null=True, blank=True)
    k3 = models.FloatField(null=True, blank=True)
    k7_1 = models.CharField(max_length=255, null=True, blank=True)
    k7_1_f = models.CharField(max_length=255, null=True, blank=True)
    k7_2 = models.CharField(max_length=255, null=True, blank=True)
    k7_2_f = models.CharField(max_length=255, null=True, blank=True)
    # descr = models.TextField(null=True, blank=True)


    def get_k1(self, hc_storage):
        # hcs - hazardous chemical substance
        # hcs_storage - 'gas_under_pressure' || 'no_pressure'
        # К1 - коэффициент, зависящий от условий хранения АХОВ, для сжатых газов К1 = 1
        # Значения К1 для изотермического хранения аммиака приведено для случая разлива (выброса) в поддон.
        # для сжатых газов К1 = 1
        if hc_storage == 'gas_under_pressure':
            k1 = 1
        else:
            k1 = self.k1
        return k1

    class Meta:
        db_table = 'HazardousChemicals'
        verbose_name = 'Коэффициеты'
        verbose_name_plural = 'Коэффициеты'

    def __str__(self):
        return '{} {}'.format(self.name, self.form)
