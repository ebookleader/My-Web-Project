from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=128, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class ResendEmailForm(forms.Form):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(ResendEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].help_text = None
