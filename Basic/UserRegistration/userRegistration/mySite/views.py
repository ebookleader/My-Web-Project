from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .models import User
from .forms import UserRegistrationForm
# Create your views here.

def index(request):
    return render(request, 'mySite/index.html')

class UserRegistrationView(CreateView):
    # 참조할 모델 클래스 정의하면 데이터 관련 부분은 이 모델을 이용하게됨
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = reverse_lazy('mySite:index')

def user_login(request):
    login_result = 'login'
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                login_result = 'not_active'
                print('not active')
        else:
            login_result = 'no_user'
            print('no user')
        return render(request, 'mySite/login.html', {'login_result': login_result})
    else:
        return render(request, 'mySite/login.html', {'login_result': login_result})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))