from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
    
class VendorModelView(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if "user_id" not in data:
            raise ValidationError({"error":"User_id should be passed."})
        serializer = VendorSerializer(data=data)
        if not serializer.is_valid():
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=data["user_id"])
        serializer.validated_data["user"] = user
        vendor = serializer.save()
        HistoricalPerformance.objects.create(vendor=vendor)
        return Response(serializer.data)

class PurchaseOrderModelView(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderModelSerializer
    
    def create(self, request, *args, **kwargs):
        vendor_id = request.data.get('vendor_code',None)
        if vendor_id is None:
            raise ValidationError("Vendor ID should be passed.")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            vendor = Vendor.objects.get(vendor_code=vendor_id)
            serializer.validated_data['vendor'] = vendor
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        if not partial:
            vendor_id = request.data.get('vendor_code',None)
            if vendor_id is None:
                raise ValidationError("Vendor ID should be passed.")
        purchase_order = PurchaseOrder.objects.get(po_number=kwargs.get('pk'))
        serializer = self.get_serializer(purchase_order, data=request.data, partial=partial)
        if serializer.is_valid():
            if not partial:
                vendor = Vendor.objects.get(vendor_code=vendor_id)
                serializer.validated_data['vendor'] = vendor
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

