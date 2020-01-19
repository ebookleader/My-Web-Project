from django.shortcuts import render
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, LoginForm, VerificationEmailForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from userRegistration import settings

from django.shortcuts import render
# Create your views here.
from .mixins import VerifyEmailMixin


def index(request):
    return render(request, 'mySite/index.html')

class UserRegistrationView(VerifyEmailMixin, CreateView):
    # 참조할 모델 클래스 정의하면 데이터 관련 부분은 이 모델을 이용하게됨
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = reverse_lazy('mySite:index')
    verify_url = '/mySite/verify'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response


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


class UserVerificationView(TemplateView):
    model = get_user_model()
    redirect_url = '/mySite/login'
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            messages.info(request, 'success')
        else:
            messages.error(request, 'failed')
        return HttpResponseRedirect(self.redirect_url)

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.object.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()
        return is_valid

class ResendVerifyEmailView(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    success_url = reverse_lazy('mySite:index')
    email_template_name = 'mySite/registration_verification.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = self.model.object.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, 'no user')
        else:
            self.send_verification_email(user)
        return super().form_valid(form)
