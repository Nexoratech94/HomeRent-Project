from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'age', 'phone', 'address', 'city', 'gender')
    search_fields = ['user__username', 'first_name', 'last_name', 'email', 'city']




from .models import OwnerProfile

@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'age', 'phone', 'city')
    search_fields = ('user__username', 'first_name', 'last_name', 'email', 'phone', 'city')
