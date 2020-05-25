from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse

from base.utils.fw_utils import get_request_param_value_bool
from serials.models import SerialNumbers


def serial_numbers(request):
    param = {}

    serial_numbers = SerialNumbers.objects.all()

    if get_request_param_value_bool(request, 'name', param):
        serial_numbers = serial_numbers.filter(Q(item_name__icontains=param['name']))

    if get_request_param_value_bool(request, 'mnufacturer', param):
        serial_numbers = serial_numbers.filter(Q(manufacturer__icontains=param['mnufacturer']))

    if get_request_param_value_bool(request, 'serial', param):
        serial_numbers = serial_numbers.filter(Q(serial_number__icontains=param['serial']))

    paginator = Paginator(serial_numbers, 20)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    return TemplateResponse(request, 'serials/serial_numbers.html',
                            context={'serials': page.object_list,
                                     'page': page,
                                     'param': param})