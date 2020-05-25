from django.contrib import admin

# Register your models here.
from autocomplete.models import AutoComplete


class ServiceAutoCompleteAdmin(admin.ModelAdmin):
    list_display = ('text', 'section')
    search_fields = ('text',)


admin.site.register(AutoComplete, ServiceAutoCompleteAdmin)