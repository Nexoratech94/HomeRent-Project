from django.urls import path
from .views import *

urlpatterns = [
    path('userlist/', userlist, name='userlist'),
    path('edit_userprofile/<int:user_id>/',edit_userprofile, name='edit_userprofile'),
    path('wonerlist/', wonerlist, name='wonerlist'),
    path('edit_wonerprofile/<int:owner_id>/', edit_wonerprofile, name='edit_wonerprofile'),
    path('add_user/', add_user, name='add_user'),
    path('add_woners/', add_woners, name='add_woners'),
]
