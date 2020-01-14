from django.urls import path
from . import views

app_name = 'mySite'

urlpatterns = [
    path('register/', views.register, name='register'),
]