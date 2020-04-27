"""todolistweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from todoapp import views

urlpatterns = [

    # admin
    path('admin/', admin.site.urls, name='admin'),

    # 처음 페이지 방문시 바로 로그인 창으로 이동
    path('', views.loginuser, name='loginuser'),
    # 디버깅용 인덱스페이지 (후에삭제)
    path('index/', views.bootindex, name='index'),

    # signup
    path('signup/', include('todoapp.urls')),
    path('resend_mail/', views.resend_mail, name='resend'),

    # mypage
    path('mypage/', views.mypage, name='mypage'),
    path('password_change/', views.password_change, name='password_change'),
    path('lock_screen/', views.lock_screen, name='lock_screen'),

    # login & logout
    path('logout/', views.logoutuser, name='logoutuser'),

    # reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # crud_todo
    path('create_monday_todo/', views.create_monday_todo, name='create_monday_todo'),
    path('current_todo/', views.current_todo, name='current_todo'),
    path('todo/<int:todo_pk>', views.todo_detail, name='todo_detail'),
    path('completed_todo/', views.completed_todo, name='completed_todo'),
    path('todo/<int:todo_pk>/delete', views.delete_todo, name='delete_todo'),
    path('todo/<int:todo_pk>/complete', views.complete_todo, name='complete_todo'),


]
