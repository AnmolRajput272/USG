# Generated by Django 4.2.11 on 2024-05-01 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='categories',
        ),
    ]