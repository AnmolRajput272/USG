# Generated by Django 4.2.11 on 2024-05-01 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0015_alter_purchaseorder_po_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_number',
            field=models.CharField(default='42a35f0e-b6cd-4ec6-9b73-85a907da4b91', editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]