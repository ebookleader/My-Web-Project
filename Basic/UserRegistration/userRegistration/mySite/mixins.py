from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from userRegistration import settings

class VerifyEmailMixin:
    email_template_name = 'mySite/registration_verification.html'
    token_generator = default_token_generator

    def send_verification_email(self, user):
        token = self.token_generator.make_token(user)
        url = self.build_verification_link(user, token)
        subject = 'Congratulations!'
        message = 'Please verify your email.{}'.format(url)
        html_message = render(self.request, self.email_template_name, {'url':url}).content.decode('utf-8')
        user.email_user(subject, message, settings.EMAIL_HOST_USER, html_message = html_message)
        messages.info(self.request, 'we send a email. please verify your email')

    def build_verification_link(self, user, token):
        return '{}/mySite/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)
