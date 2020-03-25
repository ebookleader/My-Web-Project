from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from .forms import RegistrationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.tokens import default_token_generator
from myRegistration1 import settings
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'mySite/index.html')

class RegistrationView(CreateView):
    template_name = 'mySite/user_form.html'
    model = get_user_model()
    form_class = RegistrationForm
    success_url = 'mySite/index.html'

    token_generator = default_token_generator

    def form_valid(self, form):
        response = super().form_valid(form)
        # 유효한 폼 데이터일 경우
        if form.instance:
            self.send_verification_mail(form.instance)
        return response

    def send_verification_mail(self, user):
        # 사용자 고유의 토큰을 생성한뒤 메일 보냄
        token = self.token_generator.make_token(user)
        url = self.make_verification_link(user, token)
        subject = '[MyRegistration1 Site] Verify your email'
        message = 'Click the link to verify your email. {}'.format(url)
        html_message = render(self.request, 'mySite/verification_email.html', {'url':url}).content.decode('utf-8')
        user.email_user(subject, message, settings.EMAIL_HOST_USER, html_message=html_message)

    def make_verification_link(self, user, token):
        return '{}/mySite/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)


class VerificationView(TemplateView):
    model = get_user_model()
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(**kwargs):
            return render(request, 'mySite/index.html', {'verification':True})
        else:
            return render(request, 'mySite/index.html', {'verification':False})

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('pk')
        token = kwargs.get('token')
        user = self.model.object.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()
        return is_valid