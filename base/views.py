from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from base.models import ServiceOrder, ServiceStatuses, ItemProvider, \
    ServiceOrderProcessing
from .forms import AddServiceOrder, UpdateServiceOrder


# Main View
@login_required
def main_page(request):
    return TemplateResponse(request, "base/main.html", context={})


@login_required
def view_order_document(request, order_id):
    order = ServiceOrder.objects.get(pk=order_id)
    context = {'order': order}
    return TemplateResponse(request, 'base/orders/document.html', context=context)


@login_required
def show_order(request, template_doc='base/orders/document.html'):
    order = AddServiceOrder(request.POST)
    # print(order)
    context = {}
    if order.is_valid():
        context = {'order': order.cleaned_data}
    else:
        for key in order.changed_data:
            context[key] = order[key].value()
            # print(order[key].value())
        context = {'order': context}
        # print(context)
    return TemplateResponse(request, template_doc, context=context)


@login_required
def view_order(request):
    return show_order(request, template_doc='base/orders/document.html')


def view_return_order(request):
    return show_order(request, template_doc='base/orders/return.html')


@login_required
def view_return_document(request, order_id):
    order = ServiceOrder.objects.get(pk=order_id)
    context = {'order': order}
    return TemplateResponse(request, 'base/orders/return.html', context=context)


@login_required
def view_rejection_document(request, order_id):
    order = ServiceOrder.objects.get(pk=order_id)
    context = {'order': order}
    return TemplateResponse(request, 'base/orders/rejection.html', context=context)


@login_required
def view_detail_order(request, order_id):
    order = ServiceOrder.objects.prefetch_related('itemProvider', 'parentOrder').get(pk=order_id)
    processing = order.serviceorderprocessing_set.all().order_by('-date_of_change')
    # print(processing)
    context = {'order': order, 'processing': processing}
    return TemplateResponse(request, 'base/orders/orders_detail.html', context=context)


def create_service_order(old_order, user, status=None):
    if not old_order.is_service_order:
        order = ServiceOrder()
        order.is_service_order = True
        order.author = user
        order.modify_by = user
        order.item_name = old_order.item_name
        order.manufacturer = old_order.manufacturer
        order.serial_number = old_order.serial_number
        if not status:
            order.status = ServiceStatuses.objects.get(pk=1)
        else:
            order.status = status
        order.price = old_order.price
        order.purchase_document = old_order.purchase_document
        order.comments = old_order.comments
        order.damage = old_order.damage
        order.customer = old_order.customer
        order.equipment = old_order.equipment
        order.itemProvider = old_order.itemProvider
        order.item_purchase_date = old_order.item_purchase_date
        order.count = old_order.count
        order.contact_person = 'НКТ'
        order.parentOrder = old_order
        order.save()
        return order
    return old_order


class OrderCreateForm(LoginRequiredMixin, CreateView):
    template_name = 'base/orders/CreateServiceOrder.html'
    form_class = AddServiceOrder

    def get_success_url(self):
        return reverse('update', args=(self.object.id,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.modify_by = self.request.user
        if form.instance.status.create_service_order:
            obj = form.save()
            print(obj)
            create_service_order(obj, self.request.user)
        if form.instance.status.is_terminate:
            form.instance.close_date = timezone.now()
        return super(OrderCreateForm, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderUpdateForm(LoginRequiredMixin, UpdateView):
    template_name = 'base/orders/UpdateServiceOrder.html'
    model = ServiceOrder
    form_class = UpdateServiceOrder
    success_url = '/orders/'

    def form_valid(self, form):
        modify_date = localtime(form.instance.date_of_modify).strftime("%d/%m/%Y %H:%M:%S")
        processing = ServiceOrderProcessing()
        processing.serviceOrder = form.instance
        processing.new_status = form.instance.status
        processing.author = self.request.user
        processing.comments = 'ПРЕДЕДУЩИЕ ИЗМЕНЕНИЕ:'+form.instance.modify_by.username+\
                              ' ОТ: '+modify_date

        processing.save()

        form.instance.modify_by = self.request.user

        return super(OrderUpdateForm, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderCloneForm(LoginRequiredMixin, CreateView):
    template_name = 'base/orders/CreateServiceOrder.html'
    form_class = AddServiceOrder
    model = ServiceOrder

    def get_success_url(self):
        return reverse('update', args=(self.object.id,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.modify_by = self.request.user
        if form.instance.status.create_service_order:
            obj = form.save()
            print(obj)
            create_service_order(obj, self.request.user)
        if form.instance.status.is_terminate:
            form.instance.close_date = timezone.now()
        return super(OrderCloneForm, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(OrderCloneForm, self).get_form_kwargs()
        if self.kwargs['pk']:
            new_item = get_object_or_404(ServiceOrder, pk=self.kwargs['pk'])
            new_item.pk = None
            new_item.status = None
            new_item.close_date = None
            kwargs['instance'] = new_item
        return kwargs

    # def get_form(self):
    #     form = super(OrderCloneForm, self).get_form()
    #     if self.kwargs['pk']:
    #         new_item = get_object_or_404(ServiceOrder, pk = self.kwargs['pk'])
    #         new_item.pk = None
    #         new_item.status = None
    #         form = OrderCreateForm(instance = new_item)
    #     return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def clone_order(request, order_id):
    order = ServiceOrder.objects.get(pk=order_id)
    order.pk = None
    order.status = None
    OrderCreateForm(instance=order)


def modify_order_status(request, editorder, comments, modify_order=True, provider=None, newstate=None):
    if editorder and (comments or provider or modify_order):
        if not editorder.itemProvider:
            editorder.itemProvider = provider
        if not newstate:
            newstate = editorder.status.next_state.first()

        if editorder.status == newstate or editorder.close_date:
            modify_order = False

        processing = ServiceOrderProcessing()
        processing.serviceOrder = editorder
        processing.move_to = provider
        processing.new_status = editorder.status
        processing.author = editorder.modify_by
        processing.comments = comments

        if modify_order:
            old_status = editorder.status
            editorder.status = newstate
            editorder.modify_by = request.user

            if newstate.is_terminate:
                editorder.close_date = timezone.now()

            if newstate.create_service_order:
                editorder.save()
                editorder = create_service_order(editorder, request.user, old_status)

        processing.save()
        editorder.save()
    return editorder


def get_orders(request, orders):
    def search(request_p, orders_, name, fieldname, params_dic):
        if name in request_p.POST and request_p.POST[name]:
            params_dic[name] = request_p.POST[name]
            return orders_.filter(**{fieldname: request_p.POST[name]})
        elif name in request_p.GET and request_p.GET[name]:
            params_dic[name] = request_p.GET[name]
            return orders_.filter(**{fieldname: request_p.GET[name]})
        else:
            return orders_

    param = {}

    if 'number' in request.POST and request.POST['number']:
        param['number'] = request.POST['number']
        orders = orders.filter(Q(id__exact=param['number']) | Q(adi_code__exact=param['number']))

    orders = search(request, orders, 'name', 'item_name__icontains', param)
    orders = search(request, orders, 'mnufacturer', 'manufacturer__icontains', param)
    orders = search(request, orders, 'serial', 'serial_number__icontains', param)
    orders = search(request, orders, 'phone', 'contact_phone__icontains', param)
    orders = search(request, orders, 'search_status_id', 'status__id__exact', param)


    if 'orderid' in request.POST and request.POST['orderid']:
        try:
            editorder = ServiceOrder.objects.get(pk=request.POST['orderid'])
        except ServiceOrder.DoesNotExist:
            editorder = None
        if editorder:
            comments = request.POST['comments'] if 'comments' in request.POST else None

            if 'provider' in request.POST and request.POST['provider'] and request.POST['provider'] != '0':
                provider = ItemProvider.objects.get(pk=request.POST['provider'])
            else:
                provider = None

            if 'modify' in request.POST and request.POST['modify']:
                try:
                    newstate = ServiceStatuses.objects.get(pk=request.POST['newstate'])
                    modify_order = True
                except ServiceStatuses.DoesNotExist:
                    newstate = None
                    modify_order = False

                modify_order_status(request, editorder, comments, modify_order, provider, newstate)
            else:
                if 'comments' in request.POST and request.POST['comments']:
                    comments = request.POST['comments']

                modify_order_status(request, editorder, comments, False, provider, None)


    item_provider = ItemProvider.objects.all()

    all_statuses = ServiceStatuses.objects.all()

    search_status_id = int(param['search_status_id']) if 'search_status_id' in param else -1

    paginator = Paginator(orders, 20)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    return TemplateResponse(request, 'base/orders/orders.html',
                            context={'orders': page.object_list,
                                     'page': page,
                                     'param': param,
                                     'all_statuses': all_statuses,
                                     'search_status_id':search_status_id,
                                     'item_provider': item_provider})


@login_required
def order_list(request):
    orders = ServiceOrder.objects.all()
    return get_orders(request, orders)


@login_required
def order_list_in_work(request):
    orders = ServiceOrder.objects.filter(close_date=None)
    return get_orders(request, orders)


@login_required
def order_list_finish(request):
    orders = ServiceOrder.objects.exclude(close_date=None)
    return get_orders(request, orders)


@login_required
def order_list_in_move(request):
    orders = ServiceOrder.objects.filter(status__is_need_move=True)
    return get_orders(request, orders)


@login_required
def order_list_in_client(request):
    orders = ServiceOrder.objects.filter(status__is_need_client=True)
    return get_orders(request, orders)


@login_required
def order_list_service(request):
    orders = ServiceOrder.objects.filter(is_service_order=True)
    return get_orders(request, orders)


@login_required
def order_list_in_start(request):
    orders = ServiceOrder.objects.filter(status__is_start=True)
    return get_orders(request, orders)


def get_ajax_order_info(request, order_id):
    obj = {
        'order_serial': '',
        'order_code': '',
        'order_name': '',
        'order_manuf': '',
        'order_malf': '',
        'order_comm': '',
        'order_eqpm': '',
        'order_date': '',
        'order_count': '',
        'order_contact_person': '',
        'order_contact_phone': '',
        'order_itemprov_id': '',
        'order_warranty': '',
        'order_price': '',
    }
    try:
        order = ServiceOrder.objects.get(pk=order_id)
        if order:
            date_time=''
            if order.item_purchase_date:
                date_time=order.item_purchase_date.strftime('%d/%m/%Y')
            obj = {
                'order_serial': order.serial_number,
                'order_code': order.adi_code,
                'order_name': order.item_name,
                'order_manuf': order.manufacturer,
                'order_malf': order.damage,
                'order_comm': order.comments,
                'order_eqpm': order.equipment,
                'order_date': date_time,
                'order_count': order.count,
                'order_contact_person': order.contact_person,
                'order_contact_phone': order.contact_phone,
                'order_itemprov_id': order.itemProvider.id if order.itemProvider else None,
                'order_warranty': order.warranty,
                'order_price': order.price

            }
    except ItemProvider.DoesNotExist:
        pass
    return JsonResponse(obj)


