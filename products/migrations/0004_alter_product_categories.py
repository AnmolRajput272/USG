# Generated by Django 4.2.11 on 2024-05-01 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_category_product_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(null=True, related_name='products', to='products.category'),
        ),
    ]
