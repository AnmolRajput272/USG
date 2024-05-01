from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status
from vendors.models import Vendor
from rest_framework.response import Response
from .models import *

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        query_params = self.request.query_params
        with_vendor = query_params.getlist("with_vendor")[0] if "with_vendor" in query_params else "False"
        context['with_vendor'] = True if with_vendor.lower()=="true" else False
        return context

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     if "vendor_code" not in data:
    #         raise ValidationError({"error":"vendor_code not passed"})
    #     serializer = ProductSerializer(data=data)
    #     if not serializer.is_valid():
    #         return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    #     categories = []
    #     category_ids = data.get("category_ids", [])
    #     if not isinstance(category_ids, list):
    #         raise ValidationError({"error":"category_ids should be a list."})
    #     for category_id in category_ids:
    #         try:
    #             category = Category.objects.get(id=category_id)
    #             categories.append(category)
    #         except Category.DoesNotExist:
    #             return Response({"error":f"Category with ID : {category_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.validated_data["categories"] = categories
    #     vendor = Vendor.objects.get(vendor_code=data["vendor_code"])
    #     serializer.validated_data["vendor"] = vendor
    #     serializer.save()
    #     return Response(serializer.data)
    
class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
