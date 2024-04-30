from rest_framework import serializers
from .models import Product
from vendors.serializers import VendorSerializer

class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'vendor']