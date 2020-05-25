from django.db import models

# Create your models here.
from base.models import ItemProvider, ServiceOrder


class AccompanyingSheet (models.Model):
    comment = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Комментарий')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    contact_person = models.CharField(max_length=200, verbose_name='Контактное лицо')
    contact_phone = models.CharField(max_length=50, verbose_name='Контактный телефон')
    contact_mail = models.CharField(max_length=50, verbose_name='E-mail адрес')
    customer_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название контрагента', default='ТОВ "НКТ"')
    customer_code = models.CharField(max_length=200, null=True, blank=True, verbose_name='Код контрагента')
    warranty = models.IntegerField(null=True, blank=True, verbose_name='Количество коробок', default=1)
    itemProvider = models.ForeignKey(ItemProvider, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Поставщик / Сервисный центр')

    class Meta:
        db_table = 'base_accompanyingsheet'
        verbose_name = 'Сопроводительные листы'
        ordering = ['-date_of_create', '-id']


class AccompanyingSheetItem (models.Model):
    accompanying_sheet = models.ForeignKey(AccompanyingSheet, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(ServiceOrder, on_delete=models.PROTECT, blank=True, null=True)
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name='Артикул')
    item_name = models.CharField(max_length=250, null=False, blank=False, verbose_name='Наименование')
    manufacturer = models.CharField(max_length=200, null=False, blank=False, verbose_name='Производитель')
    serial_number = models.CharField(max_length=100, blank=True, verbose_name='Серийный номер')
    malfunction = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Проблема')
    comment = models.CharField(max_length=500, null=True, blank=True, verbose_name='Комментарий')
    equipment = models.CharField(max_length=500, null=True, blank=True, verbose_name='Комплектация')
    item_purchase_date = models.DateField(null=True, default=None, blank=True, verbose_name='Дата покупки')
    count = models.IntegerField(verbose_name='Количество', default=1)

    class Meta:
        db_table = 'base_accompanyingsheetitem'