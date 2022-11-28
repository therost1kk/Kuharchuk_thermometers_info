from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializer import *


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


class ThermometersAPIView(APIView):
    def get(self, request):
        queryset = Thermometer.objects.all()
        serializer = ThermometerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ThermometerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThermometerAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            queryset = Thermometer.objects.get(id=id)
            serializer = ThermometerSerializer(queryset)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class ThermometerLocationAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            location = kwargs['location']
            queryset = Thermometer.objects.filter(location=location)
            serializer = ThermometerLocationSerializer(queryset, many=True)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class FilesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.FILES)
        file = request.FILES['csv']
        file_name = default_storage.save(file.name, file)
        response = {
            file_name: 'saved'
        }
        return Response(response)