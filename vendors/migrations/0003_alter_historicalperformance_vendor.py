# Generated by Django 4.2.11 on 2024-04-27 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_alter_historicalperformance_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_performace', to='vendors.vendor', unique=True),
        ),
    ]
