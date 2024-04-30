from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import PurchaseOrder, VendorStat
from .serializers import PurchaseOrderUpdateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

@receiver(pre_save, sender=PurchaseOrder)
def purchase_order_pre_save_signal(sender, instance, **kwargs):
    try:
        statusses = ['pending', 'cancelled', 'completed']
        old_instance = PurchaseOrder.objects.get(pk=instance.pk)
        instance._old_instance = old_instance
        
        error_message = ""
        if old_instance.status == "cancelled":
            error_message = f"Cannot update Purchase Order once cancelled."
        elif not instance.acknowledgement_date:
            error_message = f"Please Acknowledge the Purchase Order First by also passing the acknowledgement date."
        elif statusses.index(old_instance.status) > statusses.index(instance.status):
            error_message = f"Status cannot be changed from {old_instance.status} to {instance.status}"
        elif old_instance.quality_rating is not None and old_instance.quality_rating!=instance.quality_rating:
            error_message = f"Ratings cannot be changed once given."
        elif old_instance.acknowledgement_date is not None and old_instance.acknowledgement_date!=instance.acknowledgement_date:
            error_message = f"Acknowledgement date cannot be changed once given."
        elif (instance.delivery_date is not None) ^ (instance.status == "completed"):
            error_message = f"Delivery date and status:completed should be given togther."
        elif instance.quality_rating and instance.status != "completed":
            error_message = f"Quality Rating cannot be given until Delivery is completed."
        if error_message != "":
            raise ValidationError({"error":error_message})
        
    except PurchaseOrder.DoesNotExist:
        instance._old_instance = None

def status_change_stats_update(instance, historical_performance, vendor_stat):
    on_time_delivery_rate = historical_performance.on_time_delivery_rate if historical_performance.on_time_delivery_rate is not None else 100
    no_of_deliveries_completed = vendor_stat.no_of_deliveries_completed
    on_time_deliveries = (on_time_delivery_rate/100)*no_of_deliveries_completed
    present_order_is_on_time = (instance.delivery_date <= instance.expected_delivery_date)
    if present_order_is_on_time:
        on_time_deliveries += 1
    no_of_deliveries_completed += 1
    on_time_delivery_rate = (on_time_deliveries/no_of_deliveries_completed)*100
    total_no_of_pos_issued = vendor_stat.no_of_pos_issued
    fulfilment_rate = (no_of_deliveries_completed/total_no_of_pos_issued)*100 if total_no_of_pos_issued else None
    historical_performance.on_time_delivery_rate = on_time_delivery_rate
    historical_performance.fulfillment_rate = fulfilment_rate
    vendor_stat.no_of_deliveries_completed = no_of_deliveries_completed

def quality_rating_change_stats_update(instance, historical_performance, vendor_stat):
    quality_rating = instance.quality_rating
    no_of_ratings_received = vendor_stat.no_of_ratings_received + 1
    quality_rating_avg = historical_performance.quality_rating_avg if historical_performance.quality_rating_avg else 0
    sum_of_quality_ratings = (quality_rating_avg*no_of_ratings_received) + quality_rating
    quality_rating_avg = (sum_of_quality_ratings/no_of_ratings_received)*100
    historical_performance.quality_rating_avg = quality_rating_avg
    vendor_stat.no_of_ratings_received = no_of_ratings_received

def acknowledgement_date_change_stats_update(instance, historical_performance, vendor_stat):
    acknowledgement_date = instance.acknowledgement_date
    no_of_acknowledgements_given = vendor_stat.no_of_acknowledgements_given
    average_response_time = historical_performance.average_response_time if historical_performance.average_response_time else 0
    time_difference = acknowledgement_date - instance.issue_date
    sum_average_response_time = (no_of_acknowledgements_given*average_response_time) + time_difference.total_seconds()
    no_of_acknowledgements_given += 1
    average_response_time = (sum_average_response_time/no_of_acknowledgements_given)*100
    historical_performance.average_response_time = average_response_time
    vendor_stat.no_of_acknowledgements_given = no_of_acknowledgements_given

@receiver(post_save, sender=PurchaseOrder)
def purchase_order_post_save_signal(sender, instance, created, **kwargs):
    old_instance = getattr(instance, '_old_instance', None)
    fields_to_check = ["status", "quality_rating", "acknowledgement_date"]
    vendor = instance.vendor
    historical_performance = vendor.historical_performance
    vendor_stat, created_flag = VendorStat.objects.get_or_create(vendor=vendor)
    if not created:
        old_instance = PurchaseOrderUpdateSerializer(old_instance).data
        new_instance = PurchaseOrderUpdateSerializer(instance).data
        changed_fields = [field for field in fields_to_check if old_instance.get(field,None) != new_instance.get(field,None)]
        if "status" in changed_fields and instance.status == "completed":
            status_change_stats_update(instance, historical_performance, vendor_stat)
        if "quality_rating" in changed_fields:
            quality_rating_change_stats_update(instance, historical_performance, vendor_stat)
        if "acknowledgement_date" in changed_fields:
            acknowledgement_date_change_stats_update(instance, historical_performance, vendor_stat)
    else:
        vendor_stat.no_of_pos_issued = vendor_stat.no_of_pos_issued + 1
        if instance.status == "completed":
            status_change_stats_update(instance, historical_performance, vendor_stat)
        else:
            historical_performance.fulfillment_rate = (vendor_stat.no_of_deliveries_completed/vendor_stat.no_of_pos_issued)*100
        if instance.quality_rating:
            quality_rating_change_stats_update(instance, historical_performance, vendor_stat)
        if instance.acknowledgement_date:
            acknowledgement_date_change_stats_update(instance, historical_performance, vendor_stat)

    historical_performance.save()
    vendor_stat.save()