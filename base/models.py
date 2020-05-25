from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ContactTypes(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, db_index=True,
                            verbose_name='Тип контатной информации')
    col_num = models.IntegerField(null=True, default=None, verbose_name='Номер колонки для импорта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип контакта'
        verbose_name_plural = 'Типы контактной инфомации'
        ordering = ['name']


class ServiceStatuses(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, db_index=True, verbose_name='Название состояния')
    template = models.TextField(max_length=1000, blank=True, null=True, default='', verbose_name='Шаблон комментария')
    is_start = models.BooleanField(default=False, verbose_name='Начальный этап')
    is_terminate = models.BooleanField(default=False, verbose_name='Завершает обработку')
    is_need_move = models.BooleanField(default=False, verbose_name='Требует перемищения')
    is_need_client = models.BooleanField(default=False, verbose_name='Требует взаимодействия с клиентом')
    create_service_order = models.BooleanField(default=False, verbose_name='Перенести в сервисный заказ')
    next_state = models.ManyToManyField('ServiceStatuses', default=None, verbose_name='Следующие действия', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Состояние заказа'
        verbose_name_plural = 'Состояния заказов'
        ordering = ['name']


class ServiceOrder(models.Model):
    item_name = models.CharField(max_length=250, null=False, blank=False, verbose_name='Изделие/Товар')
    adi_code = models.CharField(max_length=250, null=True, blank=True, verbose_name='Код')
    manufacturer = models.CharField(max_length=200, null=False, blank=False, verbose_name='Производитель')
    price = models.FloatField(null=True, default=None, blank=True, verbose_name='Стоимость')
    item_purchase_date = models.DateField(null=True, default=None, blank=True, verbose_name='Дата покупки')
    serial_number = models.CharField(max_length=100, blank=True, verbose_name='Серийный номер')
    purchase_document = models.CharField(max_length=200, blank=True, default='',
                                         verbose_name='Документ о покупке/гарантии')
    contact_person = models.CharField(max_length=200, verbose_name='Контактное лицо')
    contact_phone = models.CharField(max_length=50, verbose_name='Контактный телефон')
    damage = models.TextField(max_length=1000, verbose_name='Повреждение/Проблема')
    comments = models.TextField(max_length=1000, blank=True, default='', verbose_name='Коментарий')
    equipment = models.TextField(max_length=500, verbose_name='Комплектация')
    date_of_receipt = models.DateTimeField(auto_now_add=True, verbose_name='Дата приема')
    status = models.ForeignKey(ServiceStatuses, on_delete=models.PROTECT, verbose_name='Статус')
    close_date = models.DateField(null=True, verbose_name='Дата закрытия заявки')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор заявки')
    is_service_order = models.BooleanField(default=False, verbose_name='Это заказ от сервиса')
    customer = models.CharField(max_length=200, null=True, blank=True, verbose_name='Поставщик (примечание)')
    itemProvider = models.ForeignKey("ItemProvider", on_delete=models.SET_NULL, blank=True, null=True,
                                 verbose_name='Поставщик')
    parentOrder = models.ForeignKey("ServiceOrder", on_delete=models.SET_NULL, blank=True, null=True,
                                     verbose_name='На основании')
    modify_by = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Последний редактор',
                                  null=True, blank=True, related_name='modifiers')
    date_of_modify = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    warranty = models.IntegerField(null=True, blank=True, verbose_name='Гарантийный срок')
    count = models.IntegerField(verbose_name='Количество', default=1)

    @property
    def pass_dates(self): return (timezone.now() - self.date_of_receipt).days

    def __str__(self):
        return f'№ {self.pk}/{self.date_of_receipt:%d-%m-%Y} {self.item_name} [{self.serial_number}] {self.manufacturer}  {self.item_purchase_date}'

    class Meta:
        verbose_name = 'Заказ на сервис'
        verbose_name_plural = 'Заказы на сервис'
        ordering = ['-date_of_receipt', '-id']


class ItemProvider(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, db_index=True, verbose_name='Название')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='Адрес')
    comments = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Комментарий')
    int_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя в базе')
    template = models.CharField(max_length=100, null=True, blank=True, verbose_name='Шаблон')
    url = models.CharField(max_length=200, null=True, blank=True, verbose_name='URL тех портала')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик или сервисный центр'
        verbose_name_plural = 'Поставщики и сервисные центы'
        ordering = ['name']


class ItemProviderContact(models.Model):
    itemProvider = models.ForeignKey(ItemProvider, on_delete=models.PROTECT)
    contactType = models.ForeignKey(ContactTypes, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100)
    contactPerson = models.CharField(max_length=200, null=True)
    is_repair_service = models.BooleanField(default=False, verbose_name='Это контакт сервисного центра')


class ServiceOrderProcessing(models.Model):
    serviceOrder = models.ForeignKey(ServiceOrder, on_delete=models.PROTECT)
    new_status = models.ForeignKey(ServiceStatuses, on_delete=models.PROTECT)
    move_to = models.ForeignKey(ItemProvider, on_delete=models.PROTECT, null=True, blank=True)
    comments = models.TextField(max_length=1000)
    date_of_change = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)


class ItemCatalog(models.Model):
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name='Артикул')
    item_name = models.CharField(max_length=250, null=False, blank=False, verbose_name='Наименование')
    parentCatalog = models.ForeignKey("ItemCatalog", on_delete=models.SET_NULL, blank=True, null=True)


class Items(models.Model):
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name='Артикул')
    item_name = models.CharField(max_length=250, null=False, blank=False, verbose_name='Наименование')
    manufacturer = models.CharField(max_length=200, null=False, blank=False, verbose_name='Производитель')
    price = models.FloatField(null=True, default=None, blank=True, verbose_name='Стоимость')
    comments = models.TextField(max_length=500, blank=True, default='', verbose_name='Коментарий')
    catalog = models.ForeignKey("ItemCatalog", on_delete=models.SET_NULL, blank=True, null=True)
    code1 = models.CharField(max_length=50, null=True, blank=True, verbose_name='Код 1')
    code2 = models.CharField(max_length=50, null=True, blank=True, verbose_name='Код 2')
    code3 = models.CharField(max_length=50, null=True, blank=True, verbose_name='Код 3')


