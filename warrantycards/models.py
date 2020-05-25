import django
from django.db import models

# Create your models here.
from django.db.models.functions import datetime

from base.models import ItemProvider, ServiceOrder


class WarrantyCard (models.Model):
    doc_num = models.IntegerField(verbose_name='Номер документа', null=True, blank=True)
    date_document = models.DateField(default=django.utils.timezone.now, verbose_name='Дата')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    buyer_person = models.CharField(max_length=200, verbose_name='Покупатель', default='Розничный', null=True, blank=True)
    buyer_phone = models.CharField(max_length=50, verbose_name='Контактный телефон', null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Гарантийные талоны'
        ordering = ['-date_of_create', '-id']


class WarrantyCardItem (models.Model):
    warrantycard = models.ForeignKey(WarrantyCard, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(ServiceOrder, on_delete=models.PROTECT, blank=True, null=True)
    item_name = models.CharField(max_length=250, null=False, blank=False, verbose_name='Наименование')
    count = models.IntegerField(verbose_name='Количество', default=1)
    serial_number = models.CharField(max_length=200, blank=True, verbose_name='Серийный номер')
    warranty = models.IntegerField(null=True, blank=True, verbose_name='Гарантийный срок')
    price = models.FloatField(null=True, default=None, blank=True, verbose_name='Цена')
    itemProvider = models.ForeignKey(ItemProvider, on_delete=models.SET_NULL, blank=True, null=True,
                                     verbose_name='Поставщик / Сервисный центр')



    class Meta:
        verbose_name = 'Пункты гарантийного талона'
