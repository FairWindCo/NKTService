from django.db import models

# Create your models here.
from base.models import ItemProvider


class SerialNumbers(models.Model):
    item_name = models.CharField(max_length=250, null=False, blank=False, verbose_name='Наименование')
    manufacturer = models.CharField(max_length=200, null=False, blank=False, verbose_name='Производитель')
    serial_number = models.CharField(max_length=100, blank=True, verbose_name='Серийный номер')
    itemProvider = models.ForeignKey(ItemProvider, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.FloatField(null=True, default=None, blank=True, verbose_name='Стоимость')
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name='Артикул у поставщика')
    item_purchase_date = models.DateField(null=True, default=None, blank=True, verbose_name='Дата покупки')
    purchase_document = models.CharField(max_length=200, blank=True, default='',
                                         verbose_name='Документ о покупке/гарантии')
    comment = models.CharField(max_length=500, null=True, blank=True, verbose_name='Комментарий')
    warranty = models.IntegerField(null=True, blank=True, verbose_name='Гарантия')
    section = models.CharField(max_length=100, null=True, blank=True, verbose_name='Раздел')

    def __str__(self):
        return f"self.item_name (self.serial_number)"

    class Meta:
        db_table = 'base_serialnumbers'
        verbose_name = 'Серийный номер'
        verbose_name_plural = 'Серийные номера'
        ordering = ['-item_purchase_date','serial_number']