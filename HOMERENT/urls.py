"""
URL configuration for HOMERENT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Home_system.urls')),
    path('Sequrity/',include('Sequrity.urls')),
    path('Blog/',include('Blog.urls')),
    path('E_commerce/',include('E_commerce.urls')),
    path('Admin_pannel/',include('Admin_pannel.urls')),
    path('User/Admin_pannel/',include('Admin_Sequrity.urls')),
    path('User/Adminpannel__userwonerInfo/',include('Adminpannel__userwonerInfo.urls')),
    path('User/Admin_ecom/',include('Admin_ecom.urls')),
    path('User/Admin_blog/',include('Admin_blog.urls')),
    path('User/StaffManagement/',include('StaffManagement.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

