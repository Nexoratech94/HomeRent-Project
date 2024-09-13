# Generated by Django 5.0.4 on 2024-05-11 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_commerce', '0021_alter_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_option',
            field=models.CharField(choices=[('sslcommerz_payment', 'SSLCommerz Payment'), ('cash_on_delivery', 'Cash on Delivery')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
