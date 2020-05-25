from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q

# Create your views here.
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from accompanying_sheets.forms import AccompanyingSheetForm, AccompanyingSheetItemFormSet
from accompanying_sheets.models import AccompanyingSheet
from base.models import ServiceStatuses
from base.utils.fw_utils import get_request_param_value_bool
from base.views import modify_order_status


def accompanying_sheets(request):
    param = {}

    accompanyingsheets = AccompanyingSheet.objects.all()

    if get_request_param_value_bool(request, 'number', param):
        accompanyingsheets = accompanyingsheets.filter(Q(id__exact=param['number']))

    paginator = Paginator(accompanyingsheets, 20)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    return TemplateResponse(request, 'accompanying_sheet/accompanying_sheets.html',
                            context={'accompanyingsheets': page.object_list,
                                     'page': page,
                                     'param': param})


def view_accompanying_sheets_t(request, ac_id, template='accompanying_sheet/list.html'):
    accompanyingsheets = AccompanyingSheet.objects.get(pk=ac_id)
    customer_name = ''
    if accompanyingsheets:
        accompanyingsheets_items = accompanyingsheets.accompanyingsheetitem_set.all()
        item_count = 0
        for item in accompanyingsheets_items:
            if item.count:
                item_count += item.count
            else:
                item_count += 1
        if accompanyingsheets.itemProvider:
            customer_name = accompanyingsheets.itemProvider.name
            customer_addr = accompanyingsheets.itemProvider.address
        else:
            customer_addr = ''
            customer_name = ''
    else:
        accompanyingsheets_items = ()
        item_count = 0
    return TemplateResponse(request, template,
                            context={'sheet': accompanyingsheets,
                                     'sheet_items': accompanyingsheets_items,
                                     'customer_name': customer_name,
                                     'customer_addr': customer_addr,
                                     'item_count': item_count})


def view_accompanying_sheets(request, ac_id):
    return view_accompanying_sheets_t(request, ac_id, 'accompanying_sheet/list.html')


def view_accompanying_sheets_det(request, ac_id):
    return view_accompanying_sheets_t(request, ac_id, 'accompanying_sheet/sheet_template.html')


@login_required
def edit_accompanying_sheet(request, ac_id):
    sheet = AccompanyingSheet.objects.get(pk=ac_id)
    asheet = AccompanyingSheetForm(instance=sheet)
    asheet_items = AccompanyingSheetItemFormSet(instance=asheet.instance)
    return TemplateResponse(request, 'accompanying_sheet/accompanying_sheet.html',
                            context={'form': asheet, 'form_items': asheet_items})


@login_required
def accompanying_sheet(request, ac_id=None):
    if request.method == 'POST':
        if not ac_id and 'ac_id' in request.POST:
            ac_id = request.POST['ac_id']

        if ac_id:
            sheet = AccompanyingSheet.objects.get(pk=ac_id)
            asheet = AccompanyingSheetForm(request.POST, instance=sheet)
        else:
            asheet = AccompanyingSheetForm(request.POST)


        asheet_items = AccompanyingSheetItemFormSet(request.POST, instance=asheet.instance)

        if asheet.is_bound:
            if asheet.is_valid():
                with transaction.atomic():
                    asheet.save()
                    if asheet_items.is_valid():
                        #asheet_items.data = {} #Очистка данных формы, так как при возврате на туже страницу происходит использование старых данных и задваивание записей
                        asheet_items.save()
                        asheet_items = AccompanyingSheetItemFormSet(instance=asheet.instance)
    else:
        if not ac_id:
            user = request.user
            name = user.first_name + ' ' + user.last_name
            phone = user.profile.phone
            asheet = AccompanyingSheetForm(initial={'contact_person': name, 'contact_mail': user.email,
                                                    'contact_phone': phone})
        else:
            sheet = AccompanyingSheet.objects.get(pk=ac_id)
            asheet = AccompanyingSheetForm(instance=sheet)
        asheet_items = AccompanyingSheetItemFormSet(instance=asheet.instance)
        print(asheet.instance.contact_mail)
    return TemplateResponse(request, 'accompanying_sheet/accompanying_sheet.html',
                            context={'form': asheet, 'form_items': asheet_items})






@login_required
def transfer_accompanyingsheet(request, ac_id, newstatus=None, set_item_provider=True):
    sheet = AccompanyingSheet.objects.get(pk=ac_id)
    items = sheet.accompanyingsheetitem_set.all()
    if items:
        for item in items:
            modify_item = item.item

            if modify_item:
                last_processing = modify_item.serviceorderprocessing_set.last()
                date = sheet.date_of_create.strftime('%d.%m.%Y') if sheet.date_of_create else ''
                comments = 'Сопроводительный дист № {} от {}'.format(sheet.pk, date)

                if modify_item.status==newstatus and last_processing and last_processing.comments == comments:
                    continue
                if not newstatus:
                    newstatus = modify_item.status.next_state.first()

                item_provider =modify_item.itemProvider if set_item_provider else None

                modify_order_status(request, modify_item, comments, True, item_provider, newstatus)

    response = redirect('accompanying_sheets')
    return response


def transfer_accompanyingsheet_ready_for_send(request, ac_id):
    return transfer_accompanyingsheet(request, ac_id, ServiceStatuses.objects.get(pk=5), False)


def transfer_accompanyingsheet_ready_for_recive(request, ac_id):
    return transfer_accompanyingsheet(request, ac_id, ServiceStatuses.objects.get(pk=6), False)


def transfer_accompanyingsheet_ready(request, ac_id):
    return transfer_accompanyingsheet(request, ac_id, ServiceStatuses.objects.get(pk=8))


def transfer_accompanyingsheet_on_service(request, ac_id):
    return transfer_accompanyingsheet(request, ac_id, ServiceStatuses.objects.get(pk=3), False)