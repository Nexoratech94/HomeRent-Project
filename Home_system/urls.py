

from django.urls import path
from .views import *  

urlpatterns = [
    path('',Home,name='Home'),
    path('room/', room_list,name='room'),
    path('house/<int:room_id>/', house_details, name='house_details'),
    path('profile/',profile,name='profile'),
    path('owner/view_owner_profile/', view_owner_profile, name='view_owner_profile'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('add_room/',add_room,name='add_room'),
    path('search/', search, name='search_results'),
    path('Upcoming/', Upcoming, name='Upcoming'),
    path('userorderdashborde/', userorderdashborde, name='userorderdashborde'),
    path('userorderdashborde', usertotalboking, name='userorderdetails'),
    path('transport/', transport, name='transport'),
]



