
from django.contrib import admin
from .models import RoomCategory, Location, Room

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'area_location')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_id','owner', 'description', 'house_number', 'road_number', 'block_number', 'street', 'get_booking_status')
    list_filter = ('house_type', 'bedrooms')
    search_fields = ('description', 'house_number', 'road_number', 'block_number', 'street')
    readonly_fields = ('room_id', 'get_booking_status')
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'location','owner','description','house_number', 'road_number', 'block_number', 'street', 'special_identification')
        }),
        ('Rent Details', {
            'fields': ('rental_amount', 'size', 'bedrooms', 'service_charge')
        }),
        ('Facilities', {
            'fields': ('facility1', 'facility2', 'facility3', 'facility4')
        }),
        ('Additional Information', {
            'fields': ('house_type', 'floor_number','geolocation','location_name')
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3', 'video')
        })
    )

    def get_booking_status(self, obj):
        return obj.booking_status
    get_booking_status.short_description = 'Booking Status'



from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'room', 'name', 'phone', 'address', 'email', 'booking_status']  
    list_filter = ['booking_status']
    search_fields = ['name', 'email']
    list_per_page = 20




from django.contrib import admin
from .models import ContactForm

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')
    search_fields = ('name', 'phone_number', 'email')


from django.contrib import admin
from .models import TransportRequest

@admin.register(TransportRequest)
class TransportRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email', 'pickup', 'dropoff', 'date', 'time')
    search_fields = ('name', 'email', 'pickup', 'dropoff')
    list_filter = ('date', 'time')
