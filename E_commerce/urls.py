from django.urls import path
from .views import *

urlpatterns = [
    path('medicine/', medicine, name='medicine'),
    path('medicine/<int:medicine_id>/', medicine_detail, name='medicine_detail'),
    path('E_commerce/add_to_cart/<int:medicine_id>/',add_to_cart, name='add_to_cart'),
    path('remove/<int:medicine_id>/', remove_from_cart, name='remove'),
    path('update_cart/<int:medicine_id>/', update_cart, name='update_cart'),
    path('update_cart/',update_cart_item, name='update_cart_item'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
]
