from django.urls import path

from accompanying_sheets.views import accompanying_sheet, accompanying_sheets, view_accompanying_sheets, \
    view_accompanying_sheets_det, transfer_accompanyingsheet_ready, transfer_accompanyingsheet_ready_for_send, \
    transfer_accompanyingsheet_ready_for_recive, transfer_accompanyingsheet_on_service

urlpatterns = [
    path('accompanyingsheet/', accompanying_sheet, name='accompanying_sheet'),
    path('accompsheet<int:ac_id>/', accompanying_sheet, name='edit_accompanying_sheet'),
    path('accomplist/', accompanying_sheets, name='accompanying_sheets'),
    path('viewsheet<int:ac_id>/', view_accompanying_sheets, name='view_accompanying_sheets'),
    path('viewsheet_det<int:ac_id>/', view_accompanying_sheets_det, name='view_accompanying_sheets_det'),
    path('trans_to<int:ac_id>/', transfer_accompanyingsheet_ready_for_send, name='transfer_accompanyingsheet_ready_for_send'),
    path('trans_from<int:ac_id>/', transfer_accompanyingsheet_ready_for_recive, name='transfer_accompanyingsheet_ready_for_recive'),
    path('outservice<int:ac_id>/', transfer_accompanyingsheet_ready, name='transfer_accompanyingsheet_ready'),
    path('sended<int:ac_id>/', transfer_accompanyingsheet_on_service, name='transfer_accompanyingsheet_on_service'),
]