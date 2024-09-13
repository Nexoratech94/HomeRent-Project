from django.urls import path
from .views import *

urlpatterns = [
    path('orderlist/', orderlist, name='orderlist'),
    path('invoice_view/<str:order_id>/', invoice_view, name='invoice_view'), 
    path('paidorder/', paidorder, name='paidorder'),
    path('edit_order/<str:order_id>/', edit_order, name='edit_order'),
    path('add_medicine/', add_medicine, name='add_medicine'),
    path('medicine_list/', medicine_list, name='medicine_list'),
    path('edit_medicine/<int:medicine_id>/',edit_medicine, name='edit_medicine'),
]