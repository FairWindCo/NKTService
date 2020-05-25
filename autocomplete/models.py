from django.db import models

# Create your models here.
class AutoComplete(models.Model):
    SECTIONS = (
        ('ER', 'Варианты ошибок'),
        ('CM', 'Варианты комплектации'),
        ('DM', 'Документы'),
    )
    text = models.CharField(max_length=250, null=False, blank=False, verbose_name='Наименование')
    section = models.CharField(max_length=2, choices=SECTIONS)

    class Meta:
        db_table = 'base_autocomplete'
        verbose_name = 'Настройки автодополнения'
        ordering = ['text']