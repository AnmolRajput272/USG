from rest_framework import serializers
from .models import *
from rest_framework.response import Response

class HistoricalPerformanceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ['date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

class VendorSerializer(serializers.ModelSerializer):
    historical_performance = HistoricalPerformanceModelSerializer(read_only=True)
    
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'name', 'contact_details', 'address', 'historical_performance']


class PurchaseOrderModelSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # Remove historical_performance from vendor data
    #     if data['vendor'] and 'historical_performance' in data['vendor']:
    #         del data['vendor']['historical_performance']
    #     return data

# class AddVendorSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     contact_details = serializers.CharField()
#     address = serializers.CharField()

#     def create(self, validated_data):
#         vendor = Vendor.objects.create(**validated_data)
#         historical_performance = HistoricalPerformance.objects.create(vendor=vendor)
#         vendor = VendorSerializer(vendor).data
#         vendor["historical_data"] = HistoricalPerformanceModelSerializer(historical_performance).data
#         return vendor



