"""
URL configuration for Education_Center project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView

from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='user_index'),
    path('logout/', views.logout_view, name='logout'),
    path('up_data/', views.up_data, name='up_data'),
    path('user_login/', views.user_login, name='user_login'),
    path('seed_sms/', views.seed_sms, name='seed_sms'),
    path('get_model/', views.get_model, name='get_model'),
    path('get_record/', views.get_record, name='get_record'),
]
