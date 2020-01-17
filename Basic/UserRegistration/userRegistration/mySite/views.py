from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import User
from .forms import UserRegistrationForm, LoginForm
# Create your views here.

def index(request):
    return render(request, 'mySite/index.html')

class UserRegistrationView(CreateView):
    # 참조할 모델 클래스 정의하면 데이터 관련 부분은 이 모델을 이용하게됨
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = reverse_lazy('mySite:index')

class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'mySite/login_form.html'

    # # form_invalid를 오버라이드해서 실패할경우 메시지 출력
    # def form_invalid(self, form):
    #     messages.error(self.request, 'login failed', extra_tags='danger')
    #     return super().form_invalid(form)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))