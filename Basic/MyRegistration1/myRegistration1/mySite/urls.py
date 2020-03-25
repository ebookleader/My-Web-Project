from django.urls import path
from . import views

app_name = 'mySite'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegistrationView.as_view(), name='register'),

]