import random
import string
from django.contrib import admin
from .models import Medicine, Medicine_Catagory

# Register your models here.
@admin.register(Medicine_Catagory)
class MedicineCatagoryAdmin(admin.ModelAdmin):
    list_display = ('cat_Id', 'cat_Name')


 
from .models import Medicine

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine_id', 'name', 'price', 'quantity', 'category', 'medicine_type', 'expire_date', 'medicine_company')
    list_filter = ('category', 'medicine_type', 'expire_date', 'medicine_company')
    search_fields = ('name', 'medicine_type')
    date_hierarchy = 'expire_date'



from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
admin.site.register(Cart, CartAdmin)


from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('medicine', 'quantity', 'price', 'subtotal', 'medicine_image')
    readonly_fields = ('price', 'subtotal', 'medicine_image')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'fname', 'lname', 'address', 'city_town', 'state', 'postcode_zip', 'phone_number', 'total_amount', 'payment_status', 'order_date')
    search_fields = ('order_id', 'user__username', 'fname', 'lname', 'address', 'city_town', 'state', 'postcode_zip', 'phone_number')
    list_filter = ('payment_status', 'order_date')
    readonly_fields = ('order_id', 'total_amount', 'order_date')
    inlines = [OrderItemInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.order_id:
            obj.order_id = obj.get_order_id()
        super().save_model(request, obj, form, change)

    def get_order_id(self, obj):
        return obj.get_order_id()
    get_order_id.short_description = 'Order ID'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'medicine', 'quantity', 'price', 'subtotal', 'medicine_image')
    search_fields = ('order__order_id', 'medicine__name')
    readonly_fields = ('price', 'subtotal', 'medicine_image')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
