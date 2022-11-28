from rest_framework import serializers
from .models import *


class ThermometerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thermometer
        fields = "__all__"


class ThermometerLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thermometer
        fields = ('name', 'location', 'temperature')
