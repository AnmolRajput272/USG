from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.exceptions import ValidationError

# class ListVendors(APIView):
#     permission_classes = []
#     authentication_classes = []

#     def get(self, request):
#         vendors = Vendor.objects.all()
#         vendors = VendorSerializer(vendors, many=True).data
#         return Response(vendors)
    
# class AddVendor(APIView):
#     permission_classes = []
#     authentication_classes = []

#     def post(self, request):
#         data = request.data
#         serializer = AddVendorSerializer(data=data)
#         if not serializer.is_valid():
#             return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         vendor = serializer.save()
#         return Response(vendor)
    
class VendorModelView(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def perform_create(self, serializer):
        vendor = serializer.save()
        HistoricalPerformance.objects.create(vendor=vendor)
        return Response(serializer.validated_data)

class PurchaseOrderModelView(ModelViewSet):
    permission_classes = []
    authentication_classes = []
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
        vendor_id = request.data.get('vendor_code',None)
        if vendor_id is None:
            raise ValidationError("Vendor ID should be passed.")
        purchase_order = PurchaseOrder.objects.get(po_number=kwargs.get('pk'))
        serializer = self.get_serializer(purchase_order, data=request.data)
        if serializer.is_valid():
            vendor = Vendor.objects.get(vendor_code=vendor_id)
            serializer.validated_data['vendor'] = vendor
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)