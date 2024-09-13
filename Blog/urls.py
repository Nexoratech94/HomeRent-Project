from django.urls import path
from .views import *  

urlpatterns = [
    path('blog/', blog, name='blog'),
    path('blogdetails/<int:blog_id>/',blog_details, name='blogdetails'),
    path('leave_comment/<int:blog_id>/',leave_comment, name='leave_comment'),
]
