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

handler400 = 'todoapp.views.error_400'
handler403 = 'todoapp.views.error_403'
handler404 = 'todoapp.views.error_404'
# handler500 = 'todoapp.views.error_500' #후에 수정
handler503 = 'todoapp.views.error_503'

urlpatterns = [

    # admin
    path('admin/', admin.site.urls, name='admin'),

    # 처음 페이지 방문시 바로 로그인 창으로 이동
    path('', views.index, name='index'),
    path('starto/', views.bootindex, name='home'),

    # signup
    path('signup/', include('todoapp.urls')),
    path('resend_mail/', views.resend_mail, name='resend'),

    # mypage
    path('mypage/', views.mypage, name='mypage'),
    path('lock_screen/', views.lock_screen, name='lock_screen'),
    path('before_modify', views.before_modify_user, name='before_modify_user'),
    path('modify_mypage', views.modify_mypage, name='modify_mypage'),
    path('delete_user', views.delete_user, name='delete_user'),

    # login & logout
    path('loginuser/', views.loginuser, name='loginuser'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),

    # reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # crud_todo
    path('todo/create/<slug:day>', views.todo_create, name='todo_create'),
    path('completed_todo/', views.completed_todo, name='completed_todo'),
    path('todo/<int:todo_pk>/complete', views.complete_todo, name='complete_todo'),
    path('todo/<int:todo_pk>/delete', views.todo_delete, name='todo_delete'),
]
