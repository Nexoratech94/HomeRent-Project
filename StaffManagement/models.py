import uuid
from django.db import models

class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    nid_number = models.CharField(max_length=20, unique=True)
    father_nid = models.CharField(max_length=20, blank=True, null=True)
    mother_nid = models.CharField(max_length=20, blank=True, null=True)
    staff_id = models.CharField(max_length=100, unique=True)
    joining_date = models.DateField()
    leaving_time = models.TimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff'),
        ('Room Cleaners', 'Room Cleaners'),
        ('Servants', 'Servants'),
        ('Accountant', 'Accountant'),
        ('Receptionist', 'Receptionist'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    on_duty = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes')
    image = models.ImageField(upload_to='staff_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            # Generate a unique staff_id starting with "ST-"
            self.staff_id = f"ST-{uuid.uuid4().hex[:4]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
