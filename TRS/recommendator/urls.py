from django.contrib import admin
from django.urls import path
from recommendator import views

urlpatterns = [
    path('',views.home),
    path('ft/',views.find_technician,name="ft"),
]
