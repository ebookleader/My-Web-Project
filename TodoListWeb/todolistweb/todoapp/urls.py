from django.urls import path
from . import views

urlpatterns = [
    path('', views.signupuser, name='signupuser'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate_account, name='activate'),
]