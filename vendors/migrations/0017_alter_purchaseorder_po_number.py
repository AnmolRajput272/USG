# Generated by Django 4.2.11 on 2024-05-01 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0016_alter_purchaseorder_po_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_number',
            field=models.CharField(default='bfd19c52-7ae3-466c-a851-b82d9eec55bd', editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
