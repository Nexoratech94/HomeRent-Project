from django.urls import path
from .views import *

urlpatterns = [
   path('admin_pannel/', admin_panel, name='admin_pannel'),
   path('update-booking-status/<int:booking_id>/', update_booking_status, name='update_booking_status'),
   path('Accept_all_booking/', Accept_all_booking, name='Accept_all_booking'),
   path('all_booking/', all_booking, name='all_booking'),
   path('edit_booking/', edit_booking, name='edit_booking'),
   path('Admin_pannel/delete_booking/<int:booking_id>/', delete_booking, name='delete_booking'),
   path('Admin_pannel/edit_booking/<int:booking_id>/', edit_book, name='edit_book'),
   path('rooms/', rooms, name='rooms'),
   path('rooms/add_rooms/', add_rooms, name='add_rooms'),
   path('Admin_pannel/rooms/edit_room/<int:room_id>/',edit_rooms, name='edit_rooms'),
   path('Admin_pannel/rooms/delete_room/<int:room_id>/',delete_rooms, name='delete_rooms'),
   path('calendar/', calendar, name='calendar'),
   path('maintain/maintain/', maintain, name='maintain'),
   path('adminmassge/',requestmassge, name='adminmassge'),
]