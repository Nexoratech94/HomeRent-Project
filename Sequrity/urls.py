from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('verify-email/<int:user_id>/<str:otp>/', verify_email, name='verify_email'),
    path('logout/', user_logout, name='logout'),
    path('woner-registration/', woner_registration, name='woner_registration'),
    path('woner-login/', woner_login, name='woner_login'),
    path('forgotpassword/', ownwerforget_pass, name='forgot'),
    path('user_forgot_password/', user_forgot_password, name='user_forgot_password'),

]   
