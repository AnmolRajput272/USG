# Generated by Django 4.2.11 on 2024-05-01 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0014_alter_purchaseorder_po_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_number',
            field=models.CharField(default='1561bb0a-a733-4efc-b51a-b336f1e433c8', editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
