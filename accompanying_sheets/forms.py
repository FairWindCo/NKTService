from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.db.models import Q
from django.forms import ModelForm, inlineformset_factory

from base.models import ServiceOrder
from accompanying_sheets.models import AccompanyingSheet, AccompanyingSheetItem


class AccompanyingSheetForm(ModelForm):
    class Meta:
        model = AccompanyingSheet
        fields = ('itemProvider', 'contact_person', 'comment',
                  'contact_phone', 'contact_mail', 'customer_name', 'customer_code', 'warranty')

    def __init__(self, *args, **kwargs):
        super(AccompanyingSheetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab('Заказ', 'itemProvider', 'customer_name', 'customer_code', css_id='tab1'),
                Tab('Контактная информация', 'contact_person', 'contact_phone', 'contact_mail', css_id='tab3'),
                Tab('Проблема/Комплектация', 'comment', 'warranty', css_id='tab4'),

            ),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )

        )


class AccompanyingSheetItemsFormSet(ModelForm):
    item = forms.ModelChoiceField(queryset=ServiceOrder.objects.filter(Q(status__pk=8) | Q(status__pk=1)),
                                  required=False, label='Заказ на сервис')
    item_purchase_date = forms.DateField(input_formats=['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y'],
                                         widget=DatePickerInput(format='%d/%m/%Y'), required=False,
                                         label='Дата покупки')

    class Meta:
        model = AccompanyingSheetItem
        fields = ('item',
                  'item_name', 'code', 'manufacturer',
                  'serial_number', 'malfunction', 'equipment', 'comment', 'item_purchase_date', 'count')

    def __init__(self, *args, **kwargs):
        super(AccompanyingSheetItemsFormSet, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'


AccompanyingSheetItemFormSet = inlineformset_factory(AccompanyingSheet, AccompanyingSheetItem, extra=1, exclude=(),
                                                     can_delete=True, form=AccompanyingSheetItemsFormSet)
