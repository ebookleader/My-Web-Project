from django.urls import path
from . import views

app_name = 'mySite'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('user_login/', views.UserLoginView.as_view(), name='user_login'),

]