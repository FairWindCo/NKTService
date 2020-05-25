import re

from django.http import JsonResponse

from base.models import ServiceOrder, ServiceStatuses, Items, ItemProvider
from serials.models import SerialNumbers


def get_service_status_list(request, order_id):
    if 'term' in request.GET:
        tag = request.GET['term']
    else:
        tag=False
    try:
        state = ServiceOrder.objects.prefetch_related('status__next_state').get(pk=order_id)
        if state.close_date:
            # print("Close")
            return JsonResponse({})
        if state and state.status:
            objects = state.status.next_state.all()
        else:
            objects = ServiceStatuses.objects.all()
        #print(objects)
        if tag:
            objects = objects.filter(name__icontains=tag)
        list_obj = {obj.id: obj.name for obj in objects}
        # print(list_obj)
    except:
        # print("Not Found")
        list_obj={}
    # print(objects)
    # print(list_obj)
    return JsonResponse(list_obj)


def get_autocomplete_serials(request):
    def form_response(answered):
        result = [{'value': value['serial_number'],
                   'label': value['serial_number'] + ' (' + value['item_name'] + ' )',
                   'manufacturer': value['manufacturer'],
                   'item_name': value['item_name'],
                   'itemProvider_id': value['itemProvider_id'],
                   'price': value['price']} for value in answered]
        return result

    tag = request.GET['term']
    # print(tag)
    serials = SerialNumbers.objects.values('item_name', 'manufacturer', 'serial_number', 'price', 'itemProvider_id', 'purchase_document').filter(
        serial_number__icontains=tag)#.distinct('serial_number')
    service = ServiceOrder.objects.values('item_name', 'manufacturer', 'serial_number', 'price', 'itemProvider_id', 'purchase_document').filter(
        serial_number__icontains=tag)#.distinct('serial_number')

    list_obj = form_response(serials)
    if not list_obj:
        list_obj = form_response(service)
    # list_obj = {obj['serial_number']: obj for obj in serials}
    # if not list_obj:
    #     list_obj = {obj['serial_number']: obj for obj in service}
    # list_obj = [{'label': key, 'value': key, 'manufacturer': value['manufacturer'],
    #              'item_name': value['item_name']} for (key, value) in list_obj.items()]
    # print(list_obj)
    return JsonResponse(list_obj, safe=False)


def get_autocomplete_manufactures(request):
    tag = request.GET['term']
    items = Items.objects.values('manufacturer').filter(manufacturer__icontains=tag)
    serials = SerialNumbers.objects.values('manufacturer').filter(manufacturer__icontains=tag)
    service = ServiceOrder.objects.values('item_name', 'manufacturer').filter(
        item_name__icontains=tag)#.distinct('item_name')
    list_obj = {obj['manufacturer']: obj['manufacturer'] for obj in items}
    if not list_obj:
        list_obj = {obj['manufacturer']: obj['manufacturer'] for obj in serials}
        if not list_obj:
            list_obj = {obj['manufacturer']: obj['manufacturer'] for obj in service}
    # print(list_obj)
    return JsonResponse(list_obj)


def get_autocomplete_names(request):
    tag = request.GET['term']
    # print("TERM=" + tag)
    serials = SerialNumbers.objects.values('item_name', 'manufacturer').filter(
        item_name__icontains=tag)#.distinct('item_name')
    service = ServiceOrder.objects.values('item_name', 'manufacturer').filter(
        item_name__icontains=tag)#.distinct('item_name')
    items = Items.objects.values('item_name', 'manufacturer').filter(item_name__icontains=tag)#.distinct('item_name')
    # l ist_obj=service.union(items).union(serials).distinct('item_name')
    list_obj = {obj['item_name']: obj for obj in items}
    if not list_obj:
        list_obj = {obj['item_name']: obj for obj in serials}
        if not list_obj:
            list_obj = {obj['item_name']: obj for obj in service}
    list_obj = [{'label': key, 'value': key, 'manufacturer': value['manufacturer']}
                for (key, value) in list_obj.items()]
    # print(list_obj)
    # RESULT FOR SELECT2
    # result={
    #     'results': list_obj,
    #     'pagination': {'more': True}
    # }
    # print(result)
    return JsonResponse(list_obj, safe=False)


def get_item_provider_code(request, item_provider_id):
    try:
        item_provider_code = ItemProvider.objects.get(pk=item_provider_id).int_name
        if item_provider_code == None:
            item_provider_code=''
    except ItemProvider.DoesNotExist:
        item_provider_code = ''
    return JsonResponse({'code': item_provider_code})


def clear_phone_number(phone):
    return re.sub(r'\D', '', phone)

def make_call(request, phone):
    import requests
    local_phone = request.user.profile.local_phone
    if local_phone:

        response = requests.post('http://voip_command_us:fb8831d6903ab6cde23700ee8cbcb6e6@192.168.1.20:8088/ari/channels?endpoint=PJSIP/'+clear_phone_number(local_phone)+'&extension='+clear_phone_number(phone)+'&context=from-internal&callerId=CALL TO '+clear_phone_number(phone)+'&priority=1')
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error':'NO LOCAL NUMBER IN USER PROFILE'})
