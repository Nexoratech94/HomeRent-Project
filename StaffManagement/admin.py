from django.contrib import admin
from .models import Staff
from django.utils.html import mark_safe

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'nid_number', 'joining_date', 'phone_number', 'role', 'image','leaving_time')
    search_fields = ('first_name', 'last_name', 'email', 'nid_number', 'role')
    list_filter = ('role', 'joining_date')

    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return mark_safe('<img src="{url}" width="100" height="100" />'.format(url=obj.image.url) if obj.image else 'No Image')
    image_tag.short_description = 'Image'
