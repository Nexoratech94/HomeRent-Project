from django.urls import path
from .views import *  

urlpatterns = [
    path('addStaff/',addStaff,name='addStaff'),
    path('all_staff/',all_staff,name='all_staff'),
    path('edit_staff/<int:staff_id>/',edit_staff,name='edit_staff'),   
]



