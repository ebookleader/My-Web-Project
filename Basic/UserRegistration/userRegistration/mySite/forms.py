from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailField
from .validators import RegisteredEmailValidator

class UserRegistrationForm(UserCreationForm):
    class Meta:
        # settings 파일에서 AUTH_USER_MODEL이 가리키는 모델을 자동으로 찾아줌
        model = get_user_model()
        # 모델에서 폼에 보여줄 필드 정의
        # password는 UserCreationForm에 의해 자동 생성
        fields = ('email','name')

class LoginForm(AuthenticationForm):
    username = EmailField()

class VerificationEmailForm(forms.Form):
        email = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), validators=(EmailField.default_validators + [RegisteredEmailValidator()]))