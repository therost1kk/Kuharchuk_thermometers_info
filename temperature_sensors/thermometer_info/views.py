from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from .models import *


def index(request):
    thermometer_locations = Thermometer.objects.values('location').annotate(lcount=Count('location')).order_by()
    return render(request, 'index.html', {'thermometer_locations': thermometer_locations})


def thermometers_info_by_location(request, location):
    try:
        thermometers = Thermometer.objects.filter(location=location)
        thermometers_info = []
        for thermometer in thermometers:
            thermometers_info.append(
                [(str(k).capitalize().replace('_', ' '), v) for k, v in thermometer.__dict__.items() if k != '_state'])
    except ObjectDoesNotExist:
        return HttpResponse("Sorry, wrong id")
    return render(request, 'thermometers_info.html', {'thermometers': thermometers_info})

def secure(request):
    return render(request, 'secure.html')