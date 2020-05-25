from django.urls import path

from warrantycards.views import warranty_card_edit, view_warranty_card_t, view_warranty_card_det, view_warranty_cards, \
    view_check_card

urlpatterns = [
    path('warranty_card/', warranty_card_edit, name='warranty_card'),
    path('edit_warranty_card<int:ac_id>/', warranty_card_edit, name='edit_warranty_card'),
    path('view<int:ac_id>/', view_warranty_card_t, name='view_warranty_card'),
    path('check<int:ac_id>/', view_check_card, name='view_check_card'),
    path('view_det<int:ac_id>/', view_warranty_card_det, name='view_warranty_card_det'),
    path('warranty_cards/', view_warranty_cards, name='warranty_cards'),
]