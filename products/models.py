from django.db import models
from vendors.models import Vendor

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name