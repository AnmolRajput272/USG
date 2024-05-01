from rest_framework import serializers
from .models import *
from vendors.serializers import VendorSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    vendor_code = serializers.CharField(write_only=True)
    category_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'categories', 'vendor_code', 'category_ids']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vendor_field = 'vendor'
        vendor_serializer = VendorSerializer(read_only=True)
        if self.context.get("with_vendor", False):
            self.fields[vendor_field] = vendor_serializer

    def create(self, validated_data):
        vendor_code = validated_data.pop('vendor_code')
        category_ids = validated_data.pop('category_ids')
        
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
        except Vendor.DoesNotExist:
            raise serializers.ValidationError({"error": "Vendor with the provided vendor_code does not exist."})

        categories = []
        for category_id in category_ids:
            try:
                category = Category.objects.get(id=category_id)
                categories.append(category)
            except Category.DoesNotExist:
                raise serializers.ValidationError({"error": f"Category with ID: {category_id} does not exist."})
        
        validated_data['vendor'] = vendor
        validated_data['categories'] = categories  # Add categories to validated_data
        instance = super().create(validated_data)
        return instance