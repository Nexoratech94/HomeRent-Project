

from django.db import models
from django.contrib.auth.models import User
from Sequrity.models import UserProfile

class RoomCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Location(models.Model):
    area_location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.area_location
from django_google_maps.fields import GeoLocationField
 
class Room(models.Model):
    BEDROOM_CHOICES = [
        (1, '1 Bedroom'),
        (2, '2 Bedrooms'),
        (3, '3 Bedrooms'),
    ]

    room_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField()
    house_number = models.CharField(max_length=100)
    road_number = models.CharField(max_length=100)
    block_number = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    special_identification = models.CharField(max_length=200, blank=True)
    house_type = models.CharField(max_length=100)
    rental_amount = models.IntegerField()
    size = models.IntegerField()
    bedrooms = models.IntegerField(choices=BEDROOM_CHOICES)
    service_charge = models.IntegerField()
    facility1 = models.CharField(max_length=100)
    facility2 = models.CharField(max_length=100, blank=True, null=True)
    facility3 = models.CharField(max_length=100, blank=True, null=True)
    facility4 = models.CharField(max_length=100, blank=True, null=True)
    floor_number = models.IntegerField()
    image1 = models.ImageField(upload_to='room_images/')
    image2 = models.ImageField(upload_to='room_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='room_images/', blank=True, null=True)
    video = models.FileField(upload_to='room_videos/', blank=True, null=True)
    geolocation = GeoLocationField(max_length=100, default='0.0,0.0')
    location_name = models.CharField(max_length=200, blank=True, null=True) 

    def __str__(self):
        return self.description[:50]  # Just for representation, can be changed

    @property
    def booking_status(self):
        return self.booking_set.first().booking_status if self.booking_set.exists() else None

import random
import string
from django.db import models
from django.utils import timezone

import calendar

class Booking(models.Model):
    STATUS_CHOICES = (
        ('accept', 'Accepted'),
        ('reject', 'Rejected'),
        ('pending', 'Pending'),
    )

    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1, 13)]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    renter_image = models.ImageField(upload_to='booking_images/')
    nid_image = models.ImageField(upload_to='booking_images/')
    total_member = models.IntegerField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    booking_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    booking_id = models.CharField(max_length=5, unique=True, blank=True, null=True)
    booking_date = models.DateField(default=timezone.now) 
    booking_time = models.TimeField(default=timezone.now) 
    booking_month = models.CharField(max_length=2, choices=MONTH_CHOICES)

    def __str__(self):
        return f"Booking for {self.room} by {self.name}"

    def generate_booking_id(self):
        return ''.join(random.choices(string.digits, k=5))

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()
        super().save(*args, **kwargs)



from django.db import models

class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


from django.db import models

class TransportRequest(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    pickup = models.CharField(max_length=255)
    dropoff = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Transport request by {self.name} from {self.pickup} to {self.dropoff} on {self.date} at {self.time}"
