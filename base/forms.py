from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from bootstrap_datepicker_plus import DatePickerInput
from .models import ServiceOrder, ServiceStatuses, ItemProvider, ServiceOrderProcessing


class AddServiceOrder(ModelForm):
    status = forms.ModelChoiceField(queryset=ServiceStatuses.objects.filter(is_start=True),
                                    required=True, label='Статус')
    item_purchase_date = forms.DateField(input_formats=['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y'],
                                         widget=DatePickerInput(format='%d/%m/%Y'), label='Дата покупки')
    itemProvider = forms.ModelChoiceField(queryset=ItemProvider.objects.all(), required=False, label='Поставщик')

    class Meta:
        model = ServiceOrder
        fields = ('status', 'item_name', 'manufacturer', 'price', 'item_purchase_date', 'serial_number',
                  'purchase_document', 'itemProvider', 'adi_code', 'is_service_order', 'warranty', 'count',
                  'contact_person', 'contact_phone', 'damage', 'equipment', 'customer', 'comments', )

    class Media:
        js = ('base/js/autocomplete.js', )

    def __init__(self, *args, **kwargs):
        super(AddServiceOrder, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True

        self.helper.layout = Layout(
            TabHolder(
                Tab('Заказ', 'status', 'item_name', 'manufacturer', 'serial_number', 'adi_code', 'count', css_id='tab1'),
                Tab('Информация о покупке', 'item_purchase_date', 'purchase_document', 'price', 'warranty', css_id='tab2'),
                Tab('Контактная информация', 'contact_person', 'contact_phone', css_id='tab3'),
                Tab('Проблема/Комплектация', 'damage', 'equipment', css_id='tab4'),
                Tab('Другое', 'itemProvider', 'customer', 'comments','is_service_order', css_id='tab5'),
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )

        )


class UpdateServiceOrder(AddServiceOrder):
    status = forms.ModelChoiceField(queryset=ServiceStatuses.objects.all(),required=True, label='Статус')


class ModifyService(ModelForm):
    move_to = forms.ModelChoiceField(queryset=ItemProvider.objects.all(), required=False, label='Поставщик')

    class Meta:
        model = ServiceOrderProcessing
        fields = ('new_status', 'move_to', 'comments')


