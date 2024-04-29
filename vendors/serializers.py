from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from accounts.serializers import UserSerializer

class HistoricalPerformanceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ['date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

class VendorSerializer(serializers.ModelSerializer):
    historical_performance = HistoricalPerformanceModelSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['vendor_code', 'name', 'contact_details', 'address', 'historical_performance', 'user']


class PurchaseOrderModelSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderUpdateSerializer(serializers.Serializer):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]

    status = serializers.ChoiceField(allow_null=True, choices=STATUS_CHOICES)
    quality_rating = serializers.FloatField(allow_null=True)
    acknowledgement_date = serializers.DateTimeField(allow_null=True)
    delivery_date = serializers.DateTimeField(allow_null=True)


