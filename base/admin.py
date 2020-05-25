from django.contrib import admin

# Register your models here.
from base.models import ContactTypes, ServiceStatuses, ItemProvider

class ContactTypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'col_num',)
    search_fields = ('name',)


class ServiceStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_terminate', 'create_service_order', 'is_start', 'is_need_move', 'is_need_client')
    search_fields = ('name',)


class ItemProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'comments', 'int_name', 'template')
    search_fields = ('name',)

admin.site.register(ContactTypes, ContactTypesAdmin)
admin.site.register(ServiceStatuses, ServiceStatusAdmin)
admin.site.register(ItemProvider, ItemProviderAdmin)
