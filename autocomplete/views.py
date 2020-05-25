from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from autocomplete.models import AutoComplete


def get_autocomplete_list(section_name, request):
    tag = request.GET['term']
    objects = AutoComplete.objects.all().filter(section=section_name).filter(text__icontains=tag)
    list_obj = {obj.id: obj.text for obj in objects}
    # print(objects)
    # print(list_obj)
    return JsonResponse(list_obj)