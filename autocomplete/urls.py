from django.urls import path

from autocomplete.views import get_autocomplete_list

urlpatterns = [
    path('auto_errors/', lambda req: get_autocomplete_list('ER', req), name='auto_errors'),
    path('auto_complect/', lambda req: get_autocomplete_list('CM', req), name='auto_cm'),
    path('auto_docs/', lambda req: get_autocomplete_list('DM', req), name='auto_dm'),
]