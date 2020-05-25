from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse

from base.utils.fw_utils import get_request_param_value_bool
from warrantycards.forms import WarrantyCardForm, WarrantyCardItemsFormSet
from warrantycards.models import WarrantyCard


@login_required
def warranty_card_edit(request, ac_id=None):
    if request.method == 'POST':
        if not ac_id and 'ac_id' in request.POST:
            ac_id = request.POST['ac_id']

        if ac_id:
            sheet = WarrantyCard.objects.get(pk=ac_id)
            warrantycard = WarrantyCardForm(request.POST, instance=sheet)
        else:
            warrantycard = WarrantyCardForm(request.POST)
        if warrantycard.is_bound:
            if warrantycard.is_valid():
                warrantycard.save()
        warrantycard_items = WarrantyCardItemsFormSet(request.POST, instance=warrantycard.instance)

        if warrantycard.is_bound:
            if warrantycard.is_valid():
                if warrantycard_items.is_valid():
                    warrantycard_items.data = {} #Очистка данных формы, так как при возврате на туже страницу происходит использование старых данных и задваивание записей
                    warrantycard_items.save()
    else:
        if not ac_id:
            warrantycard = WarrantyCardForm()
        else:
            sheet = WarrantyCard.objects.get(pk=ac_id)
            warrantycard = WarrantyCardForm(instance=sheet)
        warrantycard_items = WarrantyCardItemsFormSet(instance=warrantycard.instance)
    return TemplateResponse(request, 'warrantycards/warrantycard.html',
                            context={'form': warrantycard, 'form_items': warrantycard_items})


def view_warranty_card_t(request, ac_id, template='warrantycards/list.html'):
    warranty_card = WarrantyCard.objects.get(pk=ac_id)
    if warranty_card:
        warranty_card_items = warranty_card.warrantycarditem_set.all()
        total_sum = 0
        for item in warranty_card_items:

            if item.count and item.price:
                total_sum += item.count*item.price
            else:
                total_sum += 0
    else:
        warranty_card_items = ()
        total_sum = 0
    return TemplateResponse(request, template,
                            context={'sheet': warranty_card,
                                     'sheet_items': warranty_card_items,
                                     'total_sum': total_sum})

def view_check_card(request, ac_id):
    return view_warranty_card_t(request, ac_id, template='warrantycards/check.html')


def view_warranty_card_det(request, ac_id):
    return view_warranty_card_t(request, ac_id, 'warrantycards/warrantycard_template.html')


def view_warranty_cards(request):
    param = {}
    warranty_cards = WarrantyCard.objects.all()

    if get_request_param_value_bool(request, 'number', param):
        warranty_cards = warranty_cards.filter(Q(id__exact=param['number']))

    paginator = Paginator(warranty_cards, 20)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    return TemplateResponse(request, 'warrantycards/warrantycards.html',
                            context={'warrantycards': page.object_list,
                                     'page': page,
                                     'param': param})