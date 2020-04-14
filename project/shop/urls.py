from django.urls import path
from . import views

urlpatterns=[
     path('shop', views.home_view, name='home')
]