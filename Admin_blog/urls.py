from django.urls import path
from .views import *

urlpatterns = [
    path('adminblog/', adminblog, name='adminblog'),
    path('add_blog/', add_blog, name='add_blog'),
    path('edit_blog/<int:id>', edit_blog, name='edit_blog'),
    path('adblog_details/', adblog_details, name='adblog_details'),
    path('delete_blog/<int:id>', delete_blog, name='delete_blog'),
    
]