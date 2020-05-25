from django.urls import path

from serials.views import serial_numbers

urlpatterns = [
    path('serial_nums/', serial_numbers, name='serial_numbers'),
]