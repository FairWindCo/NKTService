from django.urls import path

from additional_user.views import update_profile

urlpatterns = [
    path('update/', update_profile, name='update_profile'),
]