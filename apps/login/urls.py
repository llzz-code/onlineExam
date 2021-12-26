from django.contrib import admin
from django.urls import path

from login.views import Login, Logout, phone

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('phone/', phone, name='phone')
]