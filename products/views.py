from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import status
from vendors.models import Vendor
from rest_framework.response import Response
from .models import Product

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if "vendor_code" not in data:
            raise ValidationError({"error":"vendor_code not passed"})
        serializer = ProductSerializer(data=data)
        if not serializer.is_valid():
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        vendor = Vendor.objects.get(vendor_code=data["vendor_code"])
        serializer.validated_data["vendor"] = vendor
        serializer.save()
        return Response(serializer.data)
