from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.db.models import Q
from django.forms import ModelForm, inlineformset_factory

from base.models import ServiceOrder
from warrantycards.models import WarrantyCardItem, WarrantyCard


class WarrantyCardForm(ModelForm):
    class Meta:
        date_document = forms.DateField(input_formats=['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y'],
                                             widget=DatePickerInput(format='%d/%m/%Y'), required=False,
                                             label='Дата покупки')

        model = WarrantyCard
        fields = ('date_document', 'buyer_person', 'comment', 'buyer_phone', 'doc_num')

    def __init__(self, *args, **kwargs):
        super(WarrantyCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab('Заказ', 'date_document', 'buyer_person', 'buyer_phone', css_id='tab1'),
                Tab('Проблема/Комплектация/Комментарий', 'comment', 'doc_num', css_id='tab2'),

            ),
            FormActions(
                Submit('submit', 'Сохранить', css_class='button white')
            )

        )


class WarrantyCardItemFormSet(ModelForm):
    item = forms.ModelChoiceField(queryset=ServiceOrder.objects.filter(Q(status__pk=8) | Q(status__pk=1)),
                                  required=False, label='Заказ на сервис')

    class Meta:
        model = WarrantyCardItem
        fields = ('item', 'item_name',  'serial_number', 'warranty', 'itemProvider', 'count', 'price')

    def __init__(self, *args, **kwargs):
        super(WarrantyCardItemFormSet, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'

# AccompanyingSheetItemsFormSet
# AccompanyingSheetItemFormSet = inlineformset_factory(AccompanyingSheet, AccompanyingSheetItem, extra=1, exclude=(),
#                                                      can_delete=True, form=AccompanyingSheetItemsFormSet)

WarrantyCardItemsFormSet = inlineformset_factory(WarrantyCard, WarrantyCardItem, extra=1, exclude=(),
                                                     can_delete=True, form=WarrantyCardItemFormSet)
