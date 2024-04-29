from django.db import models
import uuid
from django.contrib.auth.models import User

class Vendor(models.Model):
    vendor_code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendors", null=True)

class HistoricalPerformance(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name="historical_performance", unique=True)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]

    po_number = models.CharField(primary_key=True, max_length=100, unique=True, default=str(uuid.uuid4()), editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="purchase_orders", null=True)
    order_date = models.DateTimeField()
    expected_delivery_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True)


class VendorStat(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor_stat")
    no_of_deliveries_completed = models.IntegerField(default=0)
    no_of_ratings_received = models.IntegerField(default=0)
    no_of_acknowledgements_given = models.IntegerField(default=0)
    no_of_pos_issued = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.vendor.name}"
