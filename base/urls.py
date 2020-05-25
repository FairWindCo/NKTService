from django.urls import path
from .views import OrderCreateForm, view_order_document, view_return_document, \
    order_list, \
    view_detail_order, order_list_in_work, \
    order_list_finish, order_list_in_move, order_list_in_start, order_list_in_client, order_list_service, \
    OrderUpdateForm, view_rejection_document, get_ajax_order_info, OrderCloneForm
from base.view_ajax import get_service_status_list, get_autocomplete_serials, \
    get_autocomplete_manufactures, get_autocomplete_names, get_item_provider_code, make_call

urlpatterns = [
    path('add/', OrderCreateForm.as_view(), name='add'),
    path('update/<int:pk>/', OrderUpdateForm.as_view(), name='update'),
    path('clone/<int:pk>/', OrderCloneForm.as_view(), name='clone'),
    path('id<int:order_id>/', view_order_document, name='view'),
    path('ret<int:order_id>/', view_return_document, name='ret'),
    path('rej<int:order_id>/', view_rejection_document, name='rej'),
    path('json<int:order_id>/', get_ajax_order_info, name='order_json'),

    path('det<int:order_id>/', view_detail_order, name='detail'),
    path('next<int:order_id>', get_service_status_list, name='next_state'),

    path('', order_list, name='list'),
    path('in_work/', order_list_in_work, name='list_in_work'),
    path('in_move/', order_list_in_move, name='list_in_move'),
    path('in_start/', order_list_in_start, name='list_in_start'),
    path('in_client/', order_list_in_client, name='list_in_client'),
    path('service/', order_list_service, name='list_service'),
    path('finish/', order_list_finish, name='list_finish'),

    path('prov<int:item_provider_id>/', get_item_provider_code, name='item_provider_code'),

    path('auto_items/', get_autocomplete_names, name='auto_items'),
    path('auto_manufacturers/', get_autocomplete_manufactures, name='auto_manufacturers'),
    path('auto_serials/', get_autocomplete_serials, name='auto_serials'),

    path('call/<str:phone>/', make_call, name='make_call')
]
