from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, 'todoapp/index.html')

# Signup
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todoapp/signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return render(request, 'todoapp/index.html')
        else:
            return render(request, 'todoapp/signup.html', {'form': UserCreationForm()})

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