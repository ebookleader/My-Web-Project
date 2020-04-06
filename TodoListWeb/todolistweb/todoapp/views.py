from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    return render(request, 'todoapp/index.html')

# Signup
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email',None)
        password = request.POST.get('password', None)
        password_confirm = request.POST.get('password_confirm', None)

        res_data = {}
        if not(username and password and password_confirm):
            res_data['error'] = '모든 값을 입력해야합니다. 다시 시도해주세요'
        elif password != password_confirm:
            res_data['error'] = '비밀번호가 일치하지 않습니다. 다시 시도해주세요'
        else:
            cuser = CustomUser(username=username, email=email, password=make_password(password))
            cuser.save()
        return render(request, 'todoapp/signup.html', res_data)
    # if request.method == 'GET':
    #     return render(request, 'todoapp/signup.html', {'form':UserCreationForm()})
    # else:
    #     if request.POST['password1'] == request.POST['password2']:
    #         user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
    #         user.save()
    #         login(request, user)
    #         return render(request, 'todoapp/index.html')
    #     else:
    #         return render(request, 'todoapp/signup.html', {'form': UserCreationForm()})

# Login & Logout
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todoapp/login.html', {'form': AuthenticationForm()})
        else:
            login(request, user)
            return redirect('index')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')