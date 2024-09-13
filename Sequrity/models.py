from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField(default=0)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    nid_image = models.ImageField(upload_to='nid_images/')
    profile_image = models.ImageField(upload_to='profile_images/')
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    otp = models.CharField(max_length=6, null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


 

class OwnerProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )

    REGISTRATION_STATUS_CHOICES = (
        ('reject', 'Reject'),
        ('accept', 'Accept'),
        ('pending', 'Pending')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nid_image = models.ImageField(upload_to='nid_images/')
    profile_image = models.ImageField(upload_to='profile_images/',default=None)
    registration_status = models.CharField(max_length=10, choices=REGISTRATION_STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.user.username
