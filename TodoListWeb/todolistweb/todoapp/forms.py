from django import forms
from django.forms.fields import Field
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Todo

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=128, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password confirm'

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class ResendEmailForm(forms.Form):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(ResendEmailForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].help_text = None


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']

    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['memo'].widget.attrs['class'] = 'form-control'
        self.fields['important'].widget.attrs['class'] = 'form-check-input'

    setattr(Field, 'is_checkbox', lambda self:isinstance(self.widget, forms.CheckboxInput))


