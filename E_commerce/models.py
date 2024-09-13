from decimal import Decimal
import random
import string
from django.db import models
from django.utils import timezone

class Medicine_Catagory(models.Model):
    cat_Id=models.AutoField(primary_key=True)
    cat_Name=models.CharField(max_length=100)
    def __str__(self):
        return self.cat_Name
    


class Medicine(models.Model):
    TABLET = 'Tablet'
    CAPSULE = 'Capsule'
    LIQUID = 'Liquid'
    POWDER = 'Powder'
    INJECTION = 'Injection'
    SALINE = 'Saline'

    MEDICINE_TYPE_CHOICES = [
        (TABLET, 'Tablet'),
        (CAPSULE, 'Capsule'),
        (LIQUID, 'Liquid'),
        (POWDER, 'Powder'),
        (INJECTION, 'Injection'),
        (SALINE, 'Saline'),
    ]
    
    medicine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(Medicine_Catagory, on_delete=models.CASCADE)
    medicine_type = models.CharField(max_length=10, choices=MEDICINE_TYPE_CHOICES)
    expire_date = models.DateField(null=True, blank=True, default=None)
    description_title = models.CharField(max_length=100)
    description = models.TextField()
    description_title1 = models.CharField(max_length=100)
    description1 = models.TextField()
    description_title2 = models.CharField(max_length=100)
    description2 = models.TextField()
    medicine_company = models.CharField(max_length=100)
    medicine_company_logo = models.ImageField(upload_to='images')
    medicine_image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return f"{self.name} - {self.price}"





from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Medicine, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - User: {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure that price and quantity are not None and greater than zero
        if self.price is not None and self.quantity is not None and self.price > 0 and self.quantity > 0:
            # Calculate subtotal based on quantity and unit price per piece
            self.subtotal = self.quantity * self.price
        else:
            self.subtotal = 0
        
        # Calculate total price including subtotal and delivery charge
        self.total_price = self.subtotal + self.delivery_charge
        
        super().save(*args, **kwargs)

# models.py

import random
import string
from django.db import models

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    PAYMENT_OPTION_CHOICES = (
        ('sslcommerz_payment', 'SSLCommerz Payment'),
        ('cash_on_delivery', 'Cash on Delivery'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100, default='')
    lname = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=100, blank=True)
    city_town = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode_zip = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    order_notes = models.TextField(max_length=300, default='No notes')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_option = models.CharField(max_length=20, choices=PAYMENT_OPTION_CHOICES)
    order_date = models.DateTimeField(default=timezone.now)
    order_id = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"Order #{self.order_id}"

    def generate_order_id(self):
        characters = string.ascii_uppercase + string.digits
        order_id = ''.join(random.choices(characters, k=6))
        self.order_id = order_id.upper()

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.generate_order_id()
        super().save(*args, **kwargs)

from django.db import models
from django.utils.html import mark_safe
from .models import Order,Medicine

import logging
import traceback

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        try:
            print(f"Medicine price: {self.medicine.price}")
            print(f"Quantity: {self.quantity}")
            
            # Ensure self.medicine.price and self.quantity are single values
            if isinstance(self.medicine.price, Decimal) and isinstance(self.quantity, int):
                self.subtotal = self.price * self.quantity
            else:
                # Handle the case where either self.medicine.price or self.quantity is not a single value
                # You may want to log an error or handle this differently based on your application's requirements
                raise ValueError("Invalid data type for price or quantity")
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
        
        super().save(*args, **kwargs)


    def medicine_image(self):
        return mark_safe(f'<img src="{self.medicine.medicine_image.url}" alt="{self.medicine.name}" style="max-width: 100px; max-height: 100px;" />')
    medicine_image.short_description = 'Medicine Image'

    def medicine_id(self):
        return self.medicine.Medicine_ID
    medicine_id.short_description = 'Medicine ID'
